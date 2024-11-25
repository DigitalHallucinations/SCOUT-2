# modules/Providers/HuggingFace/components/response_generator.py

import asyncio
from typing import List, Dict, Union, AsyncIterator
from tenacity import retry, stop_after_attempt, wait_exponential

from .huggingface_model_manager import HuggingFaceModelManager
from ..utils.cache_manager import CacheManager
from ..utils.logger import setup_logger


class ResponseGenerator:
    """
    Generates responses using HuggingFace models. Supports both local pipeline inference
    and ONNX Runtime-based inference if an ONNX session is available.
    """

    def __init__(self, model_manager: HuggingFaceModelManager, cache_manager: CacheManager):
        """
        Initializes the ResponseGenerator with a model manager and cache manager.

        Args:
            model_manager (HuggingFaceModelManager): The model manager instance.
            cache_manager (CacheManager): The cache manager instance.
        """
        self.model_manager = model_manager
        self.cache_manager = cache_manager
        self.logger = setup_logger()
        self.model_settings = self.model_manager.base_config.model_settings

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        model: str,
        stream: bool = True
    ) -> Union[str, AsyncIterator[str]]:
        """
        Generates a response based on the provided messages using the specified model.

        Args:
            messages (List[Dict[str, str]]): A list of messages in the conversation.
            model (str): The name of the HuggingFace model to use.
            stream (bool, optional): Whether to stream the response. Defaults to True.

        Returns:
            Union[str, AsyncIterator[str]]: The generated response as a string or an asynchronous iterator for streaming.
        """
        try:
            # Generate a unique cache key based on the input messages, model, and settings
            cache_key = self.cache_manager.generate_cache_key(messages, model, self.model_settings)
            cached_response = self.cache_manager.get(cache_key)
            if cached_response:
                self.logger.info("Returning cached response")
                return cached_response

            # Load the model if it's not already loaded
            if self.model_manager.current_model != model:
                self.logger.info(f"Loading model: {model}")
                await self.model_manager.load_model(model)

            # Determine whether to use ONNX Runtime or the local pipeline
            if model in self.model_manager.ort_sessions:
                self.logger.info("Using ONNX Runtime for inference")
                response = await self._generate_with_onnx(messages, model, stream)
            else:
                self.logger.info("Using local pipeline for inference")
                response = await self._generate_local_response(messages, model, stream)

            # Cache the response if streaming is not enabled and the response is a string
            if not stream and isinstance(response, str):
                self.cache_manager.set(cache_key, response)

            return response
        except Exception as e:
            self.logger.error(f"Error in HuggingFace API call: {str(e)}")
            raise

    async def _generate_local_response(
        self,
        messages: List[Dict[str, str]],
        model: str,
        stream: bool
    ) -> Union[str, AsyncIterator[str]]:
        """
        Generates a response using the local HuggingFace pipeline.

        Args:
            messages (List[Dict[str, str]]): The conversation messages.
            model (str): The model to use.
            stream (bool): Whether to stream the response.

        Returns:
            Union[str, AsyncIterator[str]]: The generated response.
        """
        prompt = self._convert_messages_to_prompt(messages)
        self.logger.debug(f"Generated prompt for local inference: {prompt}")

        if stream:
            return self._stream_response(await self._generate_text(prompt, model))
        else:
            return await self._generate_text(prompt, model)

    async def _generate_with_onnx(
        self,
        messages: List[Dict[str, str]],
        model: str,
        stream: bool
    ) -> Union[str, AsyncIterator[str]]:
        """
        Generates a response using ONNX Runtime.

        Args:
            messages (List[Dict[str, str]]): The conversation messages.
            model (str): The model to use.
            stream (bool): Whether to stream the response.

        Returns:
            Union[str, AsyncIterator[str]]: The generated response.
        """
        # Ensure that the requested model is currently loaded
        if self.model_manager.current_model != model:
            self.logger.info(f"Loading model for ONNX inference: {model}")
            await self.model_manager.load_model(model)

        prompt = self._convert_messages_to_prompt(messages)
        self.logger.debug(f"Generated prompt for ONNX inference: {prompt}")

        # Tokenize the prompt
        inputs = self.model_manager.tokenizer(prompt, return_tensors='np')
        input_ids = inputs['input_ids']
        attention_mask = inputs.get('attention_mask', None)

        # Prepare the inputs for ONNX Runtime
        ort_inputs = {"input_ids": input_ids}
        if attention_mask is not None:
            ort_inputs["attention_mask"] = attention_mask

        self.logger.debug(f"ONNX Runtime inputs: {ort_inputs}")

        # Run inference using ONNX Runtime
        try:
            ort_session = self.model_manager.ort_sessions.get(model)
            if ort_session is None:
                raise ValueError(f"No ONNX Runtime session found for model: {model}")

            outputs = await asyncio.to_thread(
                ort_session.run, None, ort_inputs
            )
            self.logger.debug(f"ONNX Runtime outputs: {outputs}")

            # Assuming the first output contains the generated token IDs
            generated_ids = outputs[0]
            generated_text = self.model_manager.tokenizer.decode(generated_ids[0], skip_special_tokens=True)
            self.logger.debug(f"Generated text from ONNX Runtime: {generated_text}")

            if stream:
                return self._stream_response(generated_text)
            else:
                return generated_text
        except Exception as e:
            self.logger.error(f"Error during ONNX Runtime inference: {str(e)}")
            raise

    async def _generate_text(self, prompt: str, model: str) -> str:
        """
        Generates text using the HuggingFace pipeline.

        Args:
            prompt (str): The input prompt.
            model (str): The model to use.

        Returns:
            str: The generated text.
        """
        generation_kwargs = self._get_generation_config()
        generation_kwargs.pop('prompt', None)  # Ensure 'prompt' isn't duplicated
        self.logger.debug(f"Generation kwargs: {generation_kwargs}")

        # Run the pipeline in a separate thread to avoid blocking
        try:
            output = await asyncio.to_thread(self.model_manager.pipeline, prompt, **generation_kwargs)
            self.logger.debug(f"Pipeline output: {output}")

            # Extract the generated text
            return output[0]['generated_text']
        except Exception as e:
            self.logger.error(f"Error during pipeline inference: {str(e)}")
            raise

    async def _stream_response(self, text: str) -> AsyncIterator[str]:
        """
        Streams the generated text token by token.

        Args:
            text (str): The generated text.

        Yields:
            AsyncIterator[str]: Tokens of the generated text.
        """
        for token in text.split():
            yield token + " "
            await asyncio.sleep(0)  # Yield control to the event loop

    def _convert_messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """
        Converts a list of messages into a prompt string.

        Args:
            messages (List[Dict[str, str]]): The conversation messages.

        Returns:
            str: The formatted prompt.
        """
        prompt = ""
        for message in messages:
            role = message['role']
            content = message['content']
            if role == 'system':
                prompt += f"System: {content}\n"
            elif role == 'user':
                prompt += f"Human: {content}\n"
            elif role == 'assistant':
                prompt += f"Assistant: {content}\n"
        prompt += "Assistant: "
        return prompt.strip()

    def _get_generation_config(self) -> Dict:
        """
        Retrieves the generation configuration settings.

        Returns:
            Dict: The generation configuration.
        """
        config = {
            "max_new_tokens": self.model_settings.get('max_tokens', 100),
            "temperature": self.model_settings.get('temperature', 0.7),
            "top_p": self.model_settings.get('top_p', 1.0),
            "top_k": self.model_settings.get('top_k', 50),
            "repetition_penalty": self.model_settings.get('repetition_penalty', 1.0),
            "length_penalty": self.model_settings.get('length_penalty', 1.0),
            "early_stopping": self.model_settings.get('early_stopping', False),
            "do_sample": self.model_settings.get('do_sample', False),
        }
        self.logger.debug(f"Using generation config: {config}")
        return config
