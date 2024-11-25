# modules/Providers/HuggingFace/HF_gen_response.py

import asyncio
import os
from typing import List, Dict, Union, AsyncIterator
from tenacity import retry, stop_after_attempt, wait_exponential

from .config.base_config import BaseConfig
from .config.nvme_config import NVMeConfig
from .utils.cache_manager import CacheManager
from .components.huggingface_model_manager import HuggingFaceModelManager
from .components.response_generator import ResponseGenerator
from .utils.logger import setup_logger


class HuggingFaceGenerator:
    def __init__(self, config_manager):
        self.logger = setup_logger()
        self.base_config = BaseConfig(config_manager)
        self.nvme_config = NVMeConfig()
        cache_file = os.path.join(self.base_config.model_cache_dir, "response_cache.json")
        self.cache_manager = CacheManager(cache_file)
        self.model_manager = HuggingFaceModelManager(
            self.base_config,
            self.nvme_config,
            self.cache_manager
        )
        self.response_generator = ResponseGenerator(
            self.model_manager,
            self.cache_manager
        )
        self.installed_models_file = os.path.join(self.base_config.model_cache_dir, "installed_models.json")

    async def load_model(self, model_name: str, force_download: bool = False):
        await self.model_manager.load_model(model_name, force_download)

    def unload_model(self):
        self.model_manager.unload_model()

    def get_installed_models(self) -> List[str]:
        return self.model_manager.get_installed_models()

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        model: str,
        stream: bool = True
    ) -> Union[str, AsyncIterator[str]]:
        return await self.response_generator.generate_response(messages, model, stream)

    def update_model_settings(self, new_settings: Dict):
        self.base_config.update_model_settings(new_settings)

    # NVMe Configuration Methods
    def set_nvme_offloading(self, enable: bool):
        self.nvme_config.enable_nvme_offloading(enable)

    def set_nvme_path(self, path: str):
        self.nvme_config.set_nvme_path(path)

    def set_nvme_buffer_count_param(self, count: int):
        self.nvme_config.set_nvme_buffer_count_param(count)

    def set_nvme_buffer_count_optimizer(self, count: int):
        self.nvme_config.set_nvme_buffer_count_optimizer(count)

    def set_nvme_block_size(self, size: int):
        self.nvme_config.set_nvme_block_size(size)

    def set_nvme_queue_depth(self, depth: int):
        self.nvme_config.set_nvme_queue_depth(depth)

    # Additional Feature Toggle Methods
    def set_quantization(self, quantization: str):
        self.base_config.set_quantization(quantization)

    def set_gradient_checkpointing(self, enable: bool):
        self.base_config.set_gradient_checkpointing(enable)

    def set_lora(self, enable: bool):
        self.base_config.set_lora(enable)

    def set_flash_attention(self, enable: bool):
        self.base_config.set_flash_attention(enable)

    def set_pruning(self, enable: bool):
        self.base_config.set_pruning(enable)

    def set_memory_mapping(self, enable: bool):
        self.base_config.set_memory_mapping(enable)

    def set_bfloat16(self, enable: bool):
        self.base_config.set_bfloat16(enable)

    def set_torch_compile(self, enable: bool):
        self.base_config.set_torch_compile(enable)


# Helper Functions

def setup_huggingface_generator(config_manager):
    return HuggingFaceGenerator(config_manager)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def generate_response(
    config_manager,
    messages: List[Dict[str, str]],
    model: str,
    stream: bool = True
) -> Union[str, AsyncIterator[str]]:
    generator = setup_huggingface_generator(config_manager)
    await generator.load_model(model)
    return await generator.generate_response(messages, model, stream)


async def process_response(response: Union[str, AsyncIterator[str]]) -> str:
    if isinstance(response, str):
        return response
    return "".join([chunk async for chunk in response])


def generate_response_sync(
    config_manager,
    messages: List[Dict[str, str]],
    model: str,
    stream: bool = False
) -> str:
    """
    Synchronous version of generate_response for compatibility with non-async code.
    """
    loop = asyncio.get_event_loop()
    response = loop.run_until_complete(generate_response(config_manager, messages, model, stream))
    if stream:
        return loop.run_until_complete(process_response(response))
    return response
