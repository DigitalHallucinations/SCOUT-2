# modules/Providers/provider_manager.py

import logging
from modules.speech_services.Eleven_Labs.tts import get_voices as eleven_labs_get_voices, set_voice as eleven_labs_set_voice
from modules.speech_services.GglCldSvcs.tts import get_voices as google_get_voices, set_voice as google_set_voice

logger = logging.getLogger('provider_manager.py')

class ProviderManager:
    def __init__(self, chat_component, model_manager):
        self.chat_component = chat_component
        self.model_manager = model_manager
        self.current_llm_provider = "OpenAI"
        self.current_background_provider = "OpenAI"
        self.current_model = None
        self.current_speech_provider = "Eleven Labs"
        self.use_tts = False  # Initialize TTS state
        self.voices = []
        self.switch_llm_provider(self.current_llm_provider)
        self.switch_speech_provider(self.current_speech_provider)
        self.switch_background_provider(self.current_background_provider)

    def switch_llm_provider(self, llm_provider):
        if llm_provider == "OpenAI":
            from modules.Providers.OpenAI.OA_gen_response import generate_response
            self.model_manager.set_model("gpt-4o")
        elif llm_provider == "Mistral":
            from modules.Providers.Mistral.Mistral_gen_response import generate_response    
            self.model_manager.set_model("mistral-model-name")  # Replace with actual model name
        elif llm_provider == "Google":
            from modules.Providers.Google.GG_gen_response import generate_response
            self.model_manager.set_model("gemini-1.5-pro-latest")
        elif llm_provider == "HuggingFace":
            from modules.Providers.HuggingFace.HF_gen_response import generate_response  
            self.model_manager.set_model("microsoft/DialoGPT-large")  # Updated with actual model name
        elif llm_provider in ["Anthropic"]:
            from modules.Providers.Anthropic.Anthropic_gen_response import generate_response    
            self.model_manager.set_model("anthropic-model-name")  # Replace with actual model name
        elif llm_provider in ["Local"]:
            logger.warning(f"Provider {llm_provider} is not implemented yet. Reverting to default provider OpenAI.")
            from modules.Providers.OpenAI.OA_gen_response import generate_response
            self.model_manager.set_model("gpt-4o")
        else:
            raise ValueError(f"Unknown provider: {llm_provider}")

        self.current_llm_provider = llm_provider
        self.generate_response = generate_response
        logger.info(f"Switched to LLM provider: {self.current_llm_provider}")

    def switch_speech_provider(self, speech_provider):
        if speech_provider == "Eleven Labs":
            from modules.speech_services.Eleven_Labs.tts import get_voices, set_voice, get_tts, set_tts, tts
        elif speech_provider == "Google":
            from modules.speech_services.GglCldSvcs.tts import get_voices, set_voice, get_tts, set_tts, tts
        else:
            raise ValueError(f"Unknown speech provider: {speech_provider}")

        self.get_voices = get_voices
        self.set_voice = set_voice
        self.get_tts = get_tts
        self.set_tts = set_tts
        self.tts = tts

        self.current_speech_provider = speech_provider
        logger.info(f"Switched to Speech provider: {speech_provider}")

    def switch_background_provider(self, background_provider):
        self.current_background_provider = background_provider
        # Add any additional setup required for the background provider
        logger.info(f"Switched to Background provider: {self.current_background_provider}")

    def get_current_speech_provider(self):
        return self.current_speech_provider

    def get_current_model(self):
        return self.current_model

    def get_current_llm_provider(self):
        return self.current_llm_provider

    def set_tts(self, value):
        self.use_tts = value
        logger.info(f"TTS set to: {self.use_tts}")

    def get_tts(self):
        logger.info(f"TTS status: {self.use_tts}")
        return self.use_tts

    def load_voices(self):
        if self.current_speech_provider == "Eleven Labs":
            self.voices = eleven_labs_get_voices()
        elif self.current_speech_provider == "Google":
            self.voices = google_get_voices()
        else:
            logger.error(f"Unsupported speech provider: {self.current_speech_provider}")
            self.voices = []
        logger.info(f"Loaded voices: {self.voices}")

    def get_voices(self):
        return self.voices

    def set_voice(self, voice):
        if self.current_speech_provider == "Eleven Labs":
            eleven_labs_set_voice(voice)
        elif self.current_speech_provider == "Google":
            google_set_voice(voice)
        else:
            logger.error(f"Unsupported speech provider: {self.current_speech_provider}")
