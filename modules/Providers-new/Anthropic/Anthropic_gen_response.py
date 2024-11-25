# modules/Providers/Anthropic/Anthropic_gen_response.py

import asyncio
from typing import List, Dict, Union, AsyncIterator, Optional
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from config import ConfigManager
from modules.logging.logger import setup_logger
from anthropic import AsyncAnthropic, APIError, HUMAN_PROMPT, AI_PROMPT, RateLimitError
import json

class AnthropicGenerator:
    def __init__(self, config_manager=ConfigManager):
        self.config_manager = config_manager
        self.logger = setup_logger(__name__)
        self.api_key = self.config_manager.get_anthropic_api_key()
        if not self.api_key:
            self.logger.error("Anthropic API key not found in configuration")
            raise ValueError("Anthropic API key not found in configuration")
        self.client = AsyncAnthropic(api_key=self.api_key)
        self.default_model = "claude-3-opus-20240229"
        self.streaming_enabled = True
        self.function_calling_enabled = False
        self.max_retries = 3
        self.retry_delay = 5
        self.timeout = 60

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(RateLimitError)
    )
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.0,
        stream: Optional[bool] = None,
        current_persona=None,
        functions: Optional[List[Dict]] = None,
        **kwargs
    ) -> Union[str, AsyncIterator[str]]:
        try:
            model = model or self.default_model
            stream = self.streaming_enabled if stream is None else stream
            prompt = self.convert_messages_to_prompt(messages)
            
            self.logger.info(f"Generating response with Anthropic AI using model: {model}")

            completion_params = {
                "model": model,
                "prompt": prompt,
                "max_tokens_to_sample": max_tokens,
                "temperature": temperature,
                "stream": stream,
                **kwargs
            }

            if self.function_calling_enabled and functions:
                completion_params["functions"] = functions

            if stream:
                response = await asyncio.wait_for(
                    self.client.completions.create(**completion_params),
                    timeout=self.timeout
                )
                return self.process_streaming_response(response)
            else:
                response = await asyncio.wait_for(
                    self.client.completions.create(**completion_params),
                    timeout=self.timeout
                )
                return self.process_function_call(response) if self.function_calling_enabled else response.completion

        except RateLimitError as e:
            self.logger.warning(f"Rate limit reached. Retrying: {str(e)}")
            raise
        except APIError as e:
            self.logger.error(f"Anthropic API error: {str(e)}")
            raise
        except asyncio.TimeoutError:
            self.logger.error(f"Request timed out after {self.timeout} seconds")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error with Anthropic: {str(e)}")
            raise

    def convert_messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        prompt = ""
        for message in messages:
            role = message['role']
            content = message['content']
            
            if role == 'system':
                prompt += f"{content}\n\n"
            elif role == 'user':
                prompt += f"{HUMAN_PROMPT} {content}\n\n"
            elif role == 'assistant':
                prompt += f"{AI_PROMPT} {content}\n\n"
        
        prompt += f"{AI_PROMPT}"
        return prompt

    async def process_streaming_response(self, response) -> AsyncIterator[str]:
        async for chunk in response:
            if chunk.completion:
                yield chunk.completion
            await asyncio.sleep(0)

    async def process_response(self, response: Union[str, AsyncIterator[str]]) -> str:
        if isinstance(response, str):
            return response
        else:
            full_response = ""
            async for chunk in response:
                full_response += chunk
            return full_response

    def process_function_call(self, response):
        if hasattr(response, 'function_call'):
            return {
                "function_call": {
                    "name": response.function_call.name,
                    "arguments": json.loads(response.function_call.arguments)
                }
            }
        return response.completion

    def set_streaming(self, enabled: bool):
        self.streaming_enabled = enabled
        self.logger.info(f"Streaming {'enabled' if enabled else 'disabled'}")

    def set_function_calling(self, enabled: bool):
        self.function_calling_enabled = enabled
        self.logger.info(f"Function calling {'enabled' if enabled else 'disabled'}")

    def set_default_model(self, model: str):
        self.default_model = model
        self.logger.info(f"Default model set to: {model}")

    def set_timeout(self, timeout: int):
        self.timeout = timeout
        self.logger.info(f"Timeout set to: {timeout} seconds")

    def set_max_retries(self, max_retries: int):
        self.max_retries = max_retries
        self.logger.info(f"Max retries set to: {max_retries}")

    def set_retry_delay(self, retry_delay: int):
        self.retry_delay = retry_delay
        self.logger.info(f"Retry delay set to: {retry_delay} seconds")

def setup_anthropic_generator(config_manager: ConfigManager):
    return AnthropicGenerator(config_manager)

async def generate_response(
    config_manager: ConfigManager,
    messages: List[Dict[str, str]],
    model: Optional[str] = None,
    max_tokens: int = 4096,
    temperature: float = 0.0,
    stream: Optional[bool] = None,
    current_persona=None,
    functions: Optional[List[Dict]] = None,
    **kwargs
) -> Union[str, AsyncIterator[str]]:
    generator = setup_anthropic_generator(config_manager)
    return await generator.generate_response(messages, model, max_tokens, temperature, stream, current_persona, functions, **kwargs)

async def process_response(response: Union[str, AsyncIterator[str]]) -> str:
    generator = AnthropicGenerator(ConfigManager())
    return await generator.process_response(response)

def generate_response_sync(
    config_manager: ConfigManager,
    messages: List[Dict[str, str]],
    model: Optional[str] = None,
    stream: Optional[bool] = None,
    **kwargs
) -> str:
    """
    Synchronous version of generate_response for compatibility with non-async code.
    """
    loop = asyncio.get_event_loop()
    response = loop.run_until_complete(generate_response(config_manager, messages, model, stream=stream, **kwargs))
    if stream:
        return loop.run_until_complete(process_response(response))
    return response