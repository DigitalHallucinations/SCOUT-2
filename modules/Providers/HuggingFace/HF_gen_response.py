# gui/HuggingFace/HF_gen_response.py

import os
from typing import List, Dict, Union, Iterator
from tenacity import retry, stop_after_attempt, wait_exponential
from transformers import AutoTokenizer, AutoModelForCausalLM, TextIteratorStreamer, pipeline
from huggingface_hub import InferenceClient
from threading import Thread
from dotenv import load_dotenv
from modules.speech_services.GglCldSvcs import tts
from modules.logging.logger import setup_logger

logger = setup_logger("HF_gen_response.py")

load_dotenv()

HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HF_MODEL = "microsoft/DialoGPT-large"

headers = {"Authorization": f"Bearer {HF_API_KEY}"}

class HuggingFaceGenerator:
    def __init__(self):
        self.client = InferenceClient(token=HF_API_KEY)
        self.model = None
        self.tokenizer = None
        self.current_model = None
        self.pipeline = None

    def load_model(self, model_name: str):
        if self.current_model != model_name:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
            self.pipeline = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)
            self.current_model = model_name
            logger.info(f"Loaded model: {model_name}")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_response(self, messages: List[Dict[str, str]], model: str = HF_MODEL, max_tokens: int = 4096, temperature: float = 0.0, stream: bool = True) -> Union[str, Iterator[str]]:
        try:
            if self.client.model_exists(model):
                return self._generate_api_response(messages, model, max_tokens, temperature, stream)
            else:
                return self._generate_local_response(messages, model, max_tokens, temperature, stream)
        except Exception as e:
            logger.error(f"Error in HuggingFace API call: {str(e)}")
            raise

    def _generate_api_response(self, messages: List[Dict[str, str]], model: str, max_tokens: int, temperature: float, stream: bool) -> Union[str, Iterator[str]]:
        prompt = self._convert_messages_to_prompt(messages)
        params = {
            "max_new_tokens": max_tokens,
            "temperature": temperature,
            "return_full_text": False
        }
        
        if stream:
            response = self.client.text_generation(prompt, model=model, stream=True, **params)
            return (chunk.token.text for chunk in response)
        else:
            response = self.client.text_generation(prompt, model=model, **params)
            return response

    def _generate_local_response(self, messages: List[Dict[str, str]], model: str, max_tokens: int, temperature: float, stream: bool) -> Union[str, Iterator[str]]:
        self.load_model(model)
        prompt = self._convert_messages_to_prompt(messages)
        
        if stream:
            streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True)
            generation_kwargs = dict(
                prompt=prompt,
                max_new_tokens=max_tokens,
                temperature=temperature,
                streamer=streamer,
            )

            thread = Thread(target=self.pipeline, kwargs=generation_kwargs)
            thread.start()
            return streamer
        else:
            output = self.pipeline(prompt, max_new_tokens=max_tokens, temperature=temperature, return_full_text=False)
            return output[0]['generated_text']

    def _convert_messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
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
        prompt += "Assistant:"
        return prompt

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def generate_response(messages: List[Dict[str, str]], model: str = HF_MODEL, max_tokens: int = 4096, temperature: float = 0.0, stream: bool = True) -> Union[str, Iterator[str]]:
    generator = HuggingFaceGenerator()
    return generator.generate_response(messages, model, max_tokens, temperature, stream)

def process_response(response: Union[str, Iterator[str]]) -> str:
    if isinstance(response, str):
        return response
    return "".join(response)

# Wrapper functions to set and get the model
def set_hf_model(model_name: str):
    global HF_MODEL
    HF_MODEL = model_name 

def get_hf_model() -> str:
    return HF_MODEL

# Async function to generate response and optionally perform text-to-speech
async def async_generate_response(current_persona: Dict[str, str], message: List[Dict[str, str]], temperature_var: float, top_p_var: float = None, top_k_var: int = None):
    messages = [
        {"role": "user", "content": msg['content']} if msg['role'] == 'user' else {"role": "assistant", "content": msg['content']}
        for msg in message
    ]
    generator = HuggingFaceGenerator()
    response_data = generator.generate_response(messages, HF_MODEL, temperature=temperature_var, stream=False)
    
    response_content = process_response(response_data)

    if response_content and tts.get_tts():
        try:
            await tts.text_to_speech(response_content)
        except Exception as e:
            logger.error("Error during TTS: %s", e)

    print(response_content)

    return response_content
