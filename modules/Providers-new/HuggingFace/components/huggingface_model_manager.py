# modules/Providers/HuggingFace/components/huggingface_model_manager.py

import os
import json
import torch
import shutil
import asyncio
import traceback
import psutil
from typing import List, Dict, Optional, TYPE_CHECKING
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    AutoConfig,
    pipeline,
    BitsAndBytesConfig,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling,
)
from transformers.integrations.deepspeed import HfDeepSpeedConfig 
from accelerate import infer_auto_device_map

from ..config.base_config import BaseConfig
from ..config.nvme_config import NVMeConfig
from ..utils.logger import setup_logger
from ..utils.cache_manager import CacheManager

# Imports for advanced features
try:
    from peft import get_peft_model, LoraConfig  # Using PEFT for LoRA
except ImportError:
    get_peft_model = None
    LoraConfig = None

try:
    from flash_attn import replace_attn_with_flash_attn
except ImportError:
    replace_attn_with_flash_attn = None

try:
    import onnxruntime as ort
except ImportError:
    ort = None

from huggingface_hub import InferenceClient, HfApi, hf_hub_download
from datasets import Dataset 

# Conditional import for type checking
if TYPE_CHECKING and ort is not None:
    from onnxruntime import InferenceSession


class HuggingFaceModelManager:
    """
    Manages HuggingFace models, including loading, unloading, and fine-tuning.
    Supports both standard inference and ONNX Runtime-based inference.
    """

    def __init__(self, base_config: BaseConfig, nvme_config: NVMeConfig, cache_manager: CacheManager):
        """
        Initializes the HuggingFaceModelManager.

        Args:
            base_config (BaseConfig): The base configuration manager.
            nvme_config (NVMeConfig): The NVMe configuration manager.
            cache_manager (CacheManager): The cache manager for responses.
        """
        self.base_config = base_config
        self.nvme_config = nvme_config
        self.cache_manager = cache_manager
        self.logger = setup_logger()
        self.api_key = self.base_config.config_manager.get_huggingface_api_key()
        if not self.api_key:
            self.logger.error("HuggingFace API key not found in configuration")
            raise ValueError("HuggingFace API key not found in configuration")
        self.client = InferenceClient(token=self.api_key)
        self.model = None
        self.tokenizer = None
        self.current_model = None
        self.pipeline = None
        self.model_cache_dir = self.base_config.model_cache_dir
        self.installed_models_file = os.path.join(self.model_cache_dir, "installed_models.json")
        self.installed_models = self._load_installed_models()

        # Mapping from model names to their ONNX Runtime sessions
        self.ort_sessions: Dict[str, 'InferenceSession'] = {}

    def _load_installed_models(self) -> List[str]:
        """
        Loads the list of installed models from a JSON file.

        Returns:
            List[str]: A list of installed model names.
        """
        if not os.path.exists(self.installed_models_file):
            self.logger.info(f"installed_models.json not found. Creating a new one at {self.installed_models_file}")
            self._save_installed_models([])
            return []

        try:
            with open(self.installed_models_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            self.logger.error("Error decoding installed_models.json. Resetting to empty list.")
            self._save_installed_models([])
            return []

    def _save_installed_models(self, models: List[str]):
        """
        Saves the list of installed models to a JSON file.

        Args:
            models (List[str]): A list of model names to save.
        """
        try:
            with open(self.installed_models_file, 'w') as f:
                json.dump(models, f, indent=2)
            self.logger.info(f"Saved installed models to {self.installed_models_file}")
        except Exception as e:
            self.logger.error(f"Error saving installed models: {str(e)}")

    async def load_model(self, model_name: str, force_download: bool = False, use_onnx: bool = False, onnx_model_path: Optional[str] = None):
        """
        Loads the specified model, optionally downloading it and setting up ONNX Runtime.

        Args:
            model_name (str): The name of the model to load.
            force_download (bool, optional): Whether to force re-download the model. Defaults to False.
            use_onnx (bool, optional): Whether to use ONNX Runtime for this model. Defaults to False.
            onnx_model_path (Optional[str], optional): Path to the ONNX model file if use_onnx is True. Defaults to None.
        """
        model_path = os.path.join(self.model_cache_dir, "models--" + model_name.replace('/', '--'))
        model_loaded = False

        try:
            if not os.path.exists(model_path) or force_download:
                self.logger.info(f"Downloading model: {model_name}")
                try:
                    api = HfApi()
                    repo_files = await asyncio.to_thread(api.list_repo_files, repo_id=model_name)
                    for file in repo_files:
                        await asyncio.to_thread(
                            hf_hub_download, repo_id=model_name, filename=file, cache_dir=self.model_cache_dir
                        )
                    self.logger.info(f"Model downloaded and cached at: {model_path}")

                    # Log actual cache directory contents
                    self.logger.info(f"Actual model cache directory contents:")
                    for root, dirs, files in os.walk(self.model_cache_dir):
                        for file in files:
                            self.logger.info(os.path.join(root, file))

                except Exception as e:
                    self.logger.error(f"Error downloading model {model_name}: {str(e)}")
                    raise ValueError(f"Failed to download model {model_name}. Please check the model name and try again.")

            self.logger.info(f"Loading model: {model_name}")

            # Check for CUDA availability
            use_cuda = torch.cuda.is_available()
            device = "cuda" if use_cuda else "cpu"
            self.logger.info(f"Using device: {device}")

            # Load the config to determine the model type
            self.logger.info(f"Loading config for model: {model_name}")
            config = await asyncio.to_thread(AutoConfig.from_pretrained, model_name, cache_dir=self.model_cache_dir)
            self.logger.info(f"Loaded config: {config}")
            model_type = config.model_type
            self.logger.info(f"Model type: {model_type}")

            # Load the appropriate tokenizer based on the model type
            self.logger.info(f"Loading tokenizer for model type: {model_type}")
            try:
                if model_type == "llama":
                    from transformers import LlamaTokenizer
                    self.tokenizer = await asyncio.to_thread(
                        LlamaTokenizer.from_pretrained, model_name, cache_dir=self.model_cache_dir
                    )
                else:
                    # Default to AutoTokenizer for other model types
                    self.tokenizer = await asyncio.to_thread(
                        AutoTokenizer.from_pretrained, model_name, cache_dir=self.model_cache_dir
                    )
                self.logger.info(f"Tokenizer loaded successfully: {type(self.tokenizer)}")
            except ImportError as e:
                self.logger.error(f"Error importing tokenizer: {str(e)}")
                self.logger.info("Falling back to AutoTokenizer")
                self.tokenizer = await asyncio.to_thread(
                    AutoTokenizer.from_pretrained, model_name, cache_dir=self.model_cache_dir
                )

            self.logger.info(f"Loaded tokenizer for model {model_name}")

            # Initialize model_kwargs
            model_kwargs = {}

            # Strategy 1: Model Quantization
            quantization_config = None
            quantization = self.base_config.model_settings.get("quantization")
            if quantization == "8bit":
                quantization_config = BitsAndBytesConfig(
                    load_in_8bit=True, llm_int8_enable_fp32_cpu_offload=True
                )
            elif quantization == "4bit":
                quantization_config = BitsAndBytesConfig(
                    load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16
                )

            # Strategy 2: Offloading to CPU or NVMe
            gpu_memory = (
                torch.cuda.get_device_properties(0).total_memory - torch.cuda.memory_allocated(0)
                if use_cuda
                else 0
            )
            cpu_memory = psutil.virtual_memory().available

            max_memory = {'cpu': f"{int(cpu_memory * 0.8)}B"}
            if use_cuda:
                max_memory['cuda:0'] = f"{int(gpu_memory * 0.8)}B"

            # If NVMe offloading is enabled
            ds_config = None
            if self.nvme_config.offload_nvme:
                # Validate NVMe path
                if not os.path.exists(self.nvme_config.nvme_path):
                    self.logger.error(f"NVMe path {self.nvme_config.nvme_path} does not exist.")
                    raise ValueError(
                        f"NVMe path {self.nvme_config.nvme_path} does not exist. Please set a valid NVMe path."
                    )

                self.logger.info(
                    f"Configuring DeepSpeed for NVMe offloading with path: {self.nvme_config.nvme_path}"
                )

                ds_config = {
                    "zero_optimization": {
                        "stage": 3,
                        "offload_param": {
                            "device": "nvme",
                            "nvme_path": self.nvme_config.nvme_path,
                            "pin_memory": True,
                            "buffer_count": self.nvme_config.nvme_buffer_count_param,
                            "fast_init": True
                        },
                        "offload_optimizer": {
                            "device": "nvme",
                            "nvme_path": self.nvme_config.nvme_path,
                            "pin_memory": True,
                            "buffer_count": self.nvme_config.nvme_buffer_count_optimizer,
                            "fast_init": True
                        },
                        "overlap_comm": True,
                        "contiguous_gradients": True,
                        "sub_group_size": 1e9
                    },
                    "fp16": {
                        "enabled": True
                    },
                    "aio": {
                        "block_size": self.nvme_config.nvme_block_size,
                        "queue_depth": self.nvme_config.nvme_queue_depth,
                        "single_submit": False,
                        "overlap_events": True
                    }
                }
                self.logger.debug(f"DeepSpeed NVMe Config: {ds_config}")

                # Instantiate HfDeepSpeedConfig with the ds_config dictionary
                dschf = HfDeepSpeedConfig(ds_config)
                model_kwargs["deepspeed"] = dschf

            # Load the model initially to calculate device map
            self.logger.info(f"Calculating device map for model: {model_name}")
            initial_model = await asyncio.to_thread(
                AutoModelForCausalLM.from_pretrained,
                model_name,
                cache_dir=self.model_cache_dir,
                trust_remote_code=True,
            )
            device_map = infer_auto_device_map(
                initial_model,
                max_memory=max_memory,
                no_split_module_classes=["BloomBlock", "OPTDecoderLayer", "LlamaDecoderLayer"],
            )
            del initial_model  # Free up memory
            torch.cuda.empty_cache()

            # Common kwargs for model loading
            model_kwargs.update({
                "cache_dir": self.model_cache_dir,
                "trust_remote_code": True,
                "device_map": device_map,
            })

            # Strategy 7: Mixed Precision Training and Inference
            if self.base_config.model_settings.get("use_bfloat16", False):
                model_kwargs["torch_dtype"] = torch.bfloat16
            else:
                model_kwargs["torch_dtype"] = torch.float16

            # Add quantization_config if applicable
            if quantization_config is not None:
                model_kwargs["quantization_config"] = quantization_config

            # Strategy 4: Multi-GPU Support
            if torch.cuda.device_count() > 1:
                max_memory = {f'cuda:{i}': max_memory['cuda:0'] for i in range(torch.cuda.device_count())}
                device_map = infer_auto_device_map(
                    initial_model,
                    max_memory=max_memory,
                    no_split_module_classes=["BloomBlock", "OPTDecoderLayer", "LlamaDecoderLayer"],
                )
                model_kwargs['device_map'] = device_map

            self.logger.info(f"Loading model with custom device map and possible NVMe offloading")
            self.model = await asyncio.to_thread(
                AutoModelForCausalLM.from_pretrained,
                model_name,
                **model_kwargs
            )
            self.logger.info(f"Model loaded successfully: {type(self.model)}")

            # Strategy 5: Use FlashAttention
            if self.base_config.model_settings.get("use_flash_attention", False) and replace_attn_with_flash_attn is not None:
                self.logger.info("Applying FlashAttention optimization")
                self.model = replace_attn_with_flash_attn(self.model)

            # Strategy 6: Model Pruning
            if self.base_config.model_settings.get("use_pruning", False):
                self.logger.info("Applying model pruning")
                self._prune_model()

            # Strategy 9: Memory Mapping
            if self.base_config.model_settings.get("use_memory_mapping", False):
                self.logger.info("Loading model with memory mapping")
                model_kwargs["low_cpu_mem_usage"] = True

            # Strategy 13: Torch Compile
            if self.base_config.model_settings.get("use_torch_compile", False) and hasattr(torch, 'compile'):
                self.logger.info("Applying Torch Compile optimization")
                self.model = torch.compile(self.model)

            # Set up the pipeline
            self.pipeline = await asyncio.to_thread(
                pipeline,
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if use_cuda else -1,
            )
            self.logger.info(f"Pipeline set up successfully: {type(self.pipeline)}")

            # Initialize ONNX Runtime session if requested
            if use_onnx and ort is not None and onnx_model_path:
                if os.path.exists(onnx_model_path):
                    try:
                        ort_session = await asyncio.to_thread(
                            ort.InferenceSession, onnx_model_path,
                            providers=['CUDAExecutionProvider'] if torch.cuda.is_available() else ['CPUExecutionProvider']
                        )
                        self.ort_sessions[model_name] = ort_session
                        self.logger.info(f"ONNX Runtime session initialized for model: {model_name}")
                    except Exception as e:
                        self.logger.error(f"Failed to initialize ONNX Runtime session for {model_name}: {str(e)}")
                        # Optionally, you can decide to raise the exception or continue without ONNX
                else:
                    self.logger.error(f"ONNX model path {onnx_model_path} does not exist.")
            else:
                self.logger.info(f"ONNX Runtime not used for model: {model_name}")

            self.current_model = model_name
            model_loaded = True
            self.logger.info(f"Loaded model: {model_name} on device: {device}")

        except Exception as e:
            self.logger.error(f"Error loading model {model_name}: {str(e)}")
            self.logger.error(f"Error type: {type(e).__name__}")
            self.logger.error(f"Error args: {e.args}")
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            raise ValueError(f"Failed to load model {model_name}. Error: {str(e)}")

        finally:
            # Add the model to installed_models.json even if loading failed
            if model_name not in self.installed_models:
                self.installed_models.append(model_name)
                self._save_installed_models(self.installed_models)
                self.logger.info(f"Added {model_name} to installed models list")

            if model_loaded:
                self.logger.info(f"Model {model_name} loaded and ready")
            else:
                self.logger.warning(f"Model {model_name} added to installed list, but failed to load")

            # Log model files for debugging
            self.logger.info(f"Model files present in {model_path}:")
            if os.path.exists(model_path):
                for root, dirs, files in os.walk(model_path):
                    for file in files:
                        self.logger.info(f" - {os.path.join(root, file)}")
            else:
                self.logger.warning(f"Model path {model_path} does not exist")

        if not model_loaded:
            raise ValueError(f"Failed to load model {model_name}. See logs for details.")

    def _prune_model(self):
        """
        Strategy 6: Model Pruning
        Prunes the model to reduce size and improve inference speed.
        """
        import torch.nn.utils.prune as prune
        for module in self.model.modules():
            if isinstance(module, torch.nn.Linear):
                prune.l1_unstructured(module, name='weight', amount=0.2)
        self.logger.info("Model pruning applied successfully.")

    def unload_model(self):
        """
        Unloads the currently loaded model, freeing up resources.
        """
        if self.model:
            del self.model
            del self.tokenizer
            del self.pipeline
            torch.cuda.empty_cache()
            self.model = None
            self.tokenizer = None
            self.pipeline = None
            self.current_model = None
            self.logger.info("Model unloaded and CUDA cache cleared.")

        # Also unload any associated ONNX sessions
        if self.current_model and self.current_model in self.ort_sessions:
            del self.ort_sessions[self.current_model]
            self.logger.info(f"Unloaded ONNX Runtime session for model: {self.current_model}")

    def get_installed_models(self) -> List[str]:
        """
        Retrieves the list of installed models.

        Returns:
            List[str]: A list of installed model names.
        """
        return self.installed_models

    def remove_installed_model(self, model_name: str):
        """
        Removes an installed model from the cache and updates the installed models list.

        Args:
            model_name (str): The name of the model to remove.
        """
        model_path = os.path.join(self.model_cache_dir, "models--" + model_name.replace('/', '--'))
        if os.path.exists(model_path):
            shutil.rmtree(model_path)
            self.installed_models.remove(model_name)
            self._save_installed_models(self.installed_models)
            self.logger.info(f"Model {model_name} removed from installed models")

            # Also remove associated ONNX session if exists
            if model_name in self.ort_sessions:
                del self.ort_sessions[model_name]
                self.logger.info(f"ONNX Runtime session for model {model_name} removed")
        else:
            self.logger.warning(f"Model {model_name} not found in installed models")

    async def fine_tune_model(
        self,
        base_model: str,
        train_data: List[Dict],
        output_dir: str,
        num_train_epochs: int = 3,
        per_device_train_batch_size: int = 8,
        learning_rate: float = 5e-5,
        weight_decay: float = 0.01,
        save_steps: int = 1000,
        save_total_limit: int = 2,
    ):
        """
        Fine-tunes the specified base model on the provided training data.

        Args:
            base_model (str): The name of the base model to fine-tune.
            train_data (List[Dict]): A list of training samples.
            output_dir (str): Directory to save the fine-tuned model.
            num_train_epochs (int, optional): Number of training epochs. Defaults to 3.
            per_device_train_batch_size (int, optional): Batch size per device. Defaults to 8.
            learning_rate (float, optional): Learning rate for training. Defaults to 5e-5.
            weight_decay (float, optional): Weight decay for optimizer. Defaults to 0.01.
            save_steps (int, optional): Save checkpoint every X steps. Defaults to 1000.
            save_total_limit (int, optional): Maximum number of checkpoints to keep. Defaults to 2.
        """
        self.logger.info(f"Fine-tuning model {base_model} with {len(train_data)} samples")

        await self.load_model(base_model)

        # Prepare the dataset
        dataset = await asyncio.to_thread(Dataset.from_dict, {"text": [item["text"] for item in train_data]})
        tokenized_dataset = await asyncio.to_thread(dataset.map, self._tokenize_function, batched=True)

        # Strategy 3: Gradient Checkpointing
        if self.base_config.model_settings.get("use_gradient_checkpointing", False):
            self.model.gradient_checkpointing_enable()
            self.logger.info("Gradient checkpointing enabled.")

        # Prepare DeepSpeed configuration for fine-tuning
        ds_config = None
        if self.nvme_config.offload_nvme:
            ds_config = {
                "zero_optimization": {
                    "stage": 3,
                    "offload_param": {
                        "device": "nvme",
                        "nvme_path": self.nvme_config.nvme_path,
                        "pin_memory": True,
                        "buffer_count": self.nvme_config.nvme_buffer_count_param,
                        "fast_init": True
                    },
                    "offload_optimizer": {
                        "device": "nvme",
                        "nvme_path": self.nvme_config.nvme_path,
                        "pin_memory": True,
                        "buffer_count": self.nvme_config.nvme_buffer_count_optimizer,
                        "fast_init": True
                    },
                    "overlap_comm": True,
                    "contiguous_gradients": True,
                    "sub_group_size": 1e9
                },
                "fp16": {
                    "enabled": True
                },
                "aio": {
                    "block_size": self.nvme_config.nvme_block_size,
                    "queue_depth": self.nvme_config.nvme_queue_depth,
                    "single_submit": False,
                    "overlap_events": True
                }
            }

        # Adjust batch size if needed (Strategy 7)
        available_memory = psutil.virtual_memory().available
        if available_memory < 4 * 1024 ** 3:  # Less than 4GB
            per_device_train_batch_size = max(1, per_device_train_batch_size // 2)
            self.logger.warning("Low memory detected, reducing batch size.")

        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=num_train_epochs,
            per_device_train_batch_size=per_device_train_batch_size,
            learning_rate=learning_rate,
            weight_decay=weight_decay,
            save_steps=save_steps,
            save_total_limit=save_total_limit,
            fp16=not self.base_config.model_settings.get("use_bfloat16", False),
            bf16=self.base_config.model_settings.get("use_bfloat16", False),
            deepspeed=ds_config,  # Use DeepSpeed for fine-tuning
            logging_dir=os.path.join(output_dir, "logs"),
            logging_steps=100,
        )

        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer, mlm=False
        )

        # Strategy 1: Low-Rank Adaptation (LoRA)
        if self.base_config.model_settings.get("use_lora", False) and get_peft_model is not None and LoraConfig is not None:
            self.logger.info("Applying LoRA for efficient fine-tuning")
            lora_config = LoraConfig(
                r=8,
                lora_alpha=32,
                lora_dropout=0.1,
                target_modules=["q_proj", "v_proj"],
                bias="none",
                task_type="CAUSAL_LM"
            )
            self.model = get_peft_model(self.model, lora_config)
            self.logger.info("LoRA applied successfully.")
        elif self.base_config.model_settings.get("use_lora", False) and (get_peft_model is None or LoraConfig is None):
            self.logger.warning("PEFT is not installed. LoRA will not be applied.")

        # Strategy 20: Progressive Layer Freezing
        if hasattr(self, 'num_layers_to_freeze'):
            self._freeze_layers(self.num_layers_to_freeze)

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=tokenized_dataset,
            data_collator=data_collator,
        )

        await asyncio.to_thread(trainer.train)

        await asyncio.to_thread(self.model.save_pretrained, output_dir)
        await asyncio.to_thread(self.tokenizer.save_pretrained, output_dir)

        self.logger.info(f"Fine-tuned model saved to {output_dir}")

        self.current_model = output_dir
        self.logger.info(f"Current model updated to fine-tuned version: {output_dir}")

    def _tokenize_function(self, examples):
        """
        Tokenizes the input examples.

        Args:
            examples: A batch of examples to tokenize.

        Returns:
            Dict: Tokenized inputs.
        """
        return self.tokenizer(examples["text"], padding="max_length", truncation=True)

    def _freeze_layers(self, num_layers_to_freeze: int):
        """
        Strategy 20: Progressive Layer Freezing
        Freezes lower layers of the model during fine-tuning.

        Args:
            num_layers_to_freeze (int): Number of layers to freeze.
        """
        for idx, layer in enumerate(self.model.transformer.h):  # Adjust based on model architecture
            if idx < num_layers_to_freeze:
                for param in layer.parameters():
                    param.requires_grad = False
        self.logger.info(f"Frozen the first {num_layers_to_freeze} layers of the model.")

    def get_model_info(self, model_name: str) -> Dict:
        """
        Retrieves information about the specified model from Hugging Face Hub.

        Args:
            model_name (str): The name of the model.

        Returns:
            Dict: A dictionary containing model information.
        """
        try:
            model_info = self.client.model_info(model_name)
            info = {
                "pipeline_tag": model_info.pipeline_tag,
                "tags": model_info.tags,
                "num_parameters": model_info.num_parameters
            }
            self.logger.info(f"Retrieved model info for {model_name}: {info}")
            return info
        except Exception as e:
            self.logger.error(f"Error fetching model info for {model_name}: {str(e)}")
            return {}

    def update_model_settings(self, new_settings: Dict):
        """
        Updates the model settings in the base configuration.

        Args:
            new_settings (Dict): A dictionary of new settings to update.
        """
        self.base_config.update_model_settings(new_settings)
        self.logger.info(f"Model settings updated: {self.base_config.model_settings}") 
