# modules/Providers/Mistral/Mistral_gen_response.py

from mistralai import Mistral
from tenacity import retry, stop_after_attempt, wait_exponential
from typing import List, Dict, Union, AsyncIterator
from config import ConfigManager
from modules.logging.logger import setup_logger
import asyncio

class MistralGenerator:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.logger = setup_logger(__name__)
        self.api_key = self.config_manager.get_mistral_api_key()
        if not self.api_key:
            self.logger.error("Mistral API key not found in configuration")
            raise ValueError("Mistral API key not found in configuration")
        self.client = Mistral(api_key=self.api_key)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def generate_response(self, messages: List[Dict[str, str]], model: str = "mistral-large-latest", max_tokens: int = 4096, temperature: float = 0.0, stream: bool = True, current_persona=None, functions=None) -> Union[str, AsyncIterator[str]]:
        try:
            mistral_messages = self.convert_messages_to_mistral_format(messages)
            self.logger.info(f"Generating response with Mistral AI using model: {model}")
            response = await asyncio.to_thread(
                self.client.chat.complete,
                model=model,
                messages=mistral_messages,
                max_tokens=max_tokens,
                temperature=temperature,
                stream=stream
            )
            if stream:
                return self.process_streaming_response(response)
            else:
                return response.choices[0].message.content

        except Mistral.APIError as e:
            self.logger.error(f"Mistral API error: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error with Mistral: {str(e)}")
            raise

    def convert_messages_to_mistral_format(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        mistral_messages = []
        for message in messages:
            mistral_messages.append({
                "role": message['role'],
                "content": message['content']
            })
        return mistral_messages

    async def process_streaming_response(self, response) -> AsyncIterator[str]:
        async for chunk in response:
            if chunk.data.choices[0].delta.content:
                yield chunk.data.choices[0].delta.content
            await asyncio.sleep(0)

    async def process_response(self, response: Union[str, AsyncIterator[str]]) -> str:
        if isinstance(response, str):
            return response
        else:
            full_response = ""
            async for chunk in response:
                full_response += chunk
            return full_response

def setup_mistral_generator(config_manager: ConfigManager):
    return MistralGenerator(config_manager)

async def generate_response(config_manager: ConfigManager, messages: List[Dict[str, str]], model: str = "mistral-large-latest", max_tokens: int = 4096, temperature: float = 0.0, stream: bool = True, current_persona=None, functions=None) -> Union[str, AsyncIterator[str]]:
    generator = setup_mistral_generator(config_manager)
    return await generator.generate_response(messages, model, max_tokens, temperature, stream, current_persona, functions)

async def process_response(response: Union[str, AsyncIterator[str]]) -> str:
    generator = MistralGenerator(ConfigManager())
    return await generator.process_response(response)

def generate_response_sync(config_manager: ConfigManager, messages: List[Dict[str, str]], model: str = "mistral-large-latest", stream: bool = False) -> str:
    """
    Synchronous version of generate_response for compatibility with non-async code.
    """
    loop = asyncio.get_event_loop()
    response = loop.run_until_complete(generate_response(config_manager, messages, model, stream))
    if stream:
        return loop.run_until_complete(process_response(response))
    return response
