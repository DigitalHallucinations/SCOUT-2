# modules/Providers/HuggingFace/config/base_config.py

import os
from typing import Dict

class BaseConfig:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.model_cache_dir = self.config_manager.get_model_cache_dir()
        os.makedirs(self.model_cache_dir, exist_ok=True)
        self.model_settings = {
            'temperature': 0.7,
            'top_p': 1.0,
            'max_tokens': 100,
            'presence_penalty': 0.0,
            'frequency_penalty': 0.0
        }

    def update_model_settings(self, new_settings: Dict):
        valid_settings = ['temperature', 'top_p', 'max_tokens', 'presence_penalty', 'frequency_penalty']
        self.model_settings.update({k: v for k, v in new_settings.items() if k in valid_settings})
