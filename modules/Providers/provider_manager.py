# modules/Providers/provider_manager.py

import logging

logger = logging.getLogger('provider_manager.py')

class ProviderManager:
    def __init__(self, chat_component):
        self.chat_component = chat_component
        self.current_provider = "OpenAI"
        self.switch_provider(self.current_provider)

    def switch_provider(self, provider):
        if provider == "OpenAI":
            from modules.Providers.OpenAI.OA_gen_response import generate_response
        elif provider == "Mistral":
            from modules.Providers.Mistral.Mistral_gen_response import generate_response    
        elif provider == "Google":
            from modules.Providers.Google.GG_gen_response import generate_response
        elif provider == "HuggingFace":
            from modules.Providers.HuggingFace.HF_gen_response import generate_response  
        elif provider in ["Anthropic"]:
            from modules.Providers.Anthropic.Anthropic_gen_response import generate_response    
        elif provider in ["Local"]:
            logger.warning(f"Provider {provider} is not implemented yet. Reverting to default provider OpenAI.")
            from modules.Providers.OpenAI.OA_gen_response import generate_response
        else:
            raise ValueError(f"Unknown provider: {provider}")

        self.current_provider = provider
        self.generate_response = generate_response
        logger.info(f"Switched to provider: {self.current_provider}")