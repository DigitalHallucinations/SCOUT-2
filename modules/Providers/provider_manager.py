# modules/Providers/provider_manager.py

import logging

logger = logging.getLogger('provider_manager.py')

class ProviderManager:
    def __init__(self, chat_component):
        self.chat_component = chat_component
        self.current_llm_provider = "Anthropic"
        self.current_background_provider = "Anthropic"
        self.current_model = None
        self.current_speech_provider = "Eleven Labs"
        self.switch_llm_provider(self.current_llm_provider)
        self.switch_speech_provider(self.current_speech_provider)
        self.switch_background_provider(self.current_background_provider) 

    def switch_llm_provider(self, llm_provider):
        if llm_provider == "OpenAI":
            from modules.Providers.OpenAI.OA_gen_response import generate_response
        elif llm_provider == "Mistral":
            from modules.Providers.Mistral.Mistral_gen_response import generate_response    
        elif llm_provider == "Google":
            from modules.Providers.Google.GG_gen_response import generate_response
        elif llm_provider == "HuggingFace":
            from modules.Providers.HuggingFace.HF_gen_response import generate_response  
        elif llm_provider in ["Anthropic"]:
            from modules.Providers.Anthropic.Anthropic_gen_response import generate_response    
        elif llm_provider in ["Local"]:
            logger.warning(f"Provider {llm_provider} is not implemented yet. Reverting to default provider OpenAI.")
            from modules.Providers.OpenAI.OA_gen_response import generate_response
        else:
            raise ValueError(f"Unknown provider: {llm_provider}")

        self.current_llm_provider = llm_provider
        self.generate_response = generate_response
        logger.info(f"Switched to LLM provider: {self.current_llm_provider}")

    def switch_background_provider(self, background_provider):
        if background_provider == "OpenAI":
            from modules.Providers.OpenAI.openai_api import OpenAIAPI
            self.generate_cognitive_background_service = OpenAIAPI().generate_cognitive_background_service
        elif background_provider == "Mistral":
            from modules.Providers.Mistral.Mistral_api import MistralAPI
            self.generate_cognitive_background_service = MistralAPI().generate_cognitive_background_service
        elif background_provider == "Anthropic":
            from modules.Providers.Anthropic.Anthropic_api import AnthropicAPI
            self.generate_cognitive_background_service = AnthropicAPI().generate_cognitive_background_service
        else:
            raise ValueError(f"Unknown background provider: {background_provider}")

        self.current_background_provider = background_provider
        logger.info(f"Switched to background provider: {self.current_background_provider}")

    def get_current_background_provider(self):
        return self.current_background_provider

    def switch_speech_provider(self, speech_provider):
        self.current_speech_provider = speech_provider
        logger.info(f"Switched to speech provider: {self.current_speech_provider}")

    def set_current_model(self, model):
        self.current_model = model

    def get_current_llm_provider(self):
        return self.current_llm_provider

    def get_current_speech_provider(self):
        return self.current_speech_provider

    def get_current_model(self):
        return self.current_model