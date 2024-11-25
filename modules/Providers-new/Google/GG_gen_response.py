# modules/Providers/Google/GG_gen_response.py

import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential
from typing import List, Dict, Union, AsyncIterator
from config import ConfigManager
from modules.logging.logger import setup_logger
import asyncio

class GoogleGeminiGenerator:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.logger = setup_logger(__name__)
        self.api_key = self.config_manager.get_google_api_key()
        if not self.api_key:
            self.logger.error("Google API key not found in configuration")
            raise ValueError("Google API key not found in configuration")
        genai.configure(api_key=self.api_key)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def generate_response(self, messages: List[Dict[str, str]], model: str = "gemini-1.5-pro-latest", max_tokens: int = 32000, temperature: float = 0.0, stream: bool = True, current_persona=None, functions=None) -> Union[str, AsyncIterator[str]]:
        try:
            prompt = self.convert_messages_to_prompt(messages)
            model = genai.GenerativeModel(model_name=model)
            self.logger.info(f"Generating response with Google Gemini using model: {model}")
            
            response = await asyncio.to_thread(
                model.generate_content,
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=temperature
                ),
                stream=stream
            )

            if stream:
                return self.stream_response(response)
            else:
                return response.text

        except Exception as e:
            self.logger.error(f"Error in Google Gemini API call: {str(e)}")
            raise

    def convert_messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        prompt = ""
        for message in messages:
            role = message['role']
            content = message['content']
            
            if role == 'system':
                prompt += f"System: {content}\n\n"
            elif role == 'user':
                prompt += f"Human: {content}\n\n"
            elif role == 'assistant':
                prompt += f"Assistant: {content}\n\n"
        
        prompt += "Human: Please respond to the above context.\n\nAssistant:"
        return prompt

    async def stream_response(self, response) -> AsyncIterator[str]:
        for chunk in response:
            if chunk.text:
                yield chunk.text
            await asyncio.sleep(0)  # Allow other coroutines to run

    async def process_response(self, response) -> str:
        if isinstance(response, AsyncIterator):
            full_response = ""
            async for chunk in response:
                full_response += chunk
            return full_response
        else:
            return response

def setup_google_gemini_generator(config_manager: ConfigManager):
    return GoogleGeminiGenerator(config_manager)

async def generate_response(config_manager: ConfigManager, messages: List[Dict[str, str]], model: str = "gemini-1.5-pro-latest", max_tokens: int = 32000, temperature: float = 0.0, stream: bool = True, current_persona=None, functions=None):
    generator = setup_google_gemini_generator(config_manager)
    return await generator.generate_response(messages, model, max_tokens, temperature, stream, current_persona, functions)

async def process_response(response: Union[str, AsyncIterator[str]]) -> str:
    if isinstance(response, str):
        return response
    elif isinstance(response, AsyncIterator):
        full_response = ""
        async for chunk in response:
            full_response += chunk
        return full_response
    else:
        raise ValueError(f"Unexpected response type: {type(response)}")