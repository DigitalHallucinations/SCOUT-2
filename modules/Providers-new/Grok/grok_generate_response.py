# modules/Providers/Grok/grok_generate_response.py

from xai_sdk import Client
from typing import List, Dict, Union, AsyncIterator
from config import ConfigManager
from modules.logging.logger import setup_logger


class GrokGenerator:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.logger = setup_logger(__name__)
        self.api_key = self.config_manager.get_grok_api_key()
        if not self.api_key:
            self.logger.error("Grok API key not found in configuration")
            raise ValueError("Grok API key not found in configuration")

        # Initialize Grok Client
        self.client = Client(api_key=self.api_key)
        self.logger.info("Grok client initialized")

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        model: str = "grok-2",
        max_tokens: int = 1000,
        stream: bool = False
    ) -> Union[str, AsyncIterator[str]]:
        """
        Generates a response from Grok's model.
        :param messages: List of message dicts containing "role" and "content" keys.
        :param model: The Grok model to use. Defaults to "grok-2".
        :param max_tokens: Maximum tokens for the response.
        :param stream: If True, enables streaming of responses.
        :return: Generated response or an async iterator if streaming.
        """
        self.logger.info(f"Generating response using Grok model {model}")
        try:
            if stream:
                return self._stream_response(messages, model, max_tokens)
            else:
                return await self._get_grok_response(messages, model, max_tokens)
        
        except Exception as e:
            self.logger.error(f"Error generating Grok response: {str(e)}")
            raise

    async def _get_grok_response(
        self,
        messages: List[Dict[str, str]],
        model: str,
        max_tokens: int
    ) -> str:
        """
        Non-streaming response generation from Grok.
        """
        prompt = self._build_prompt_from_messages(messages)
        self.logger.debug(f"Sending prompt to Grok: {prompt}")
        result = await self.client.sampler.sample(prompt, max_len=max_tokens)
        response = "".join([token.token_str for token in result])
        self.logger.info(f"Grok response received: {response}")
        return response

    async def _stream_response(
        self,
        messages: List[Dict[str, str]],
        model: str,
        max_tokens: int
    ) -> AsyncIterator[str]:
        """
        Streaming response generation from Grok.
        """
        prompt = self._build_prompt_from_messages(messages)
        self.logger.debug(f"Streaming prompt to Grok: {prompt}")
        async for token in self.client.sampler.sample(prompt, max_len=max_tokens):
            yield token.token_str

    def _build_prompt_from_messages(self, messages: List[Dict[str, str]]) -> str:
        """
        Converts messages into a prompt string for Grok.
        """
        self.logger.debug(f"Building prompt from messages: {messages}")
        return "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
