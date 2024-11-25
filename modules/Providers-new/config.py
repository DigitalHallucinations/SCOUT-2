# Providers/config.py

import os
from typing import Dict, Any
from modules.logging.logger import setup_logger
from dotenv import load_dotenv, set_key, find_dotenv

class ConfigManager:
    """
    Manages configuration settings for the application, including loading
    environment variables and handling API keys for various providers.

    Attributes:
        config (Dict[str, Any]): A dictionary holding all configuration settings..
    """

    def __init__(self):
        """
        Initializes the ConfigManager by loading environment variables and loading configuration settings.

        Raises:
            ValueError: If the API key for the default provider is not found in environment variables.
        """
        # Load environment variables from .env file
        load_dotenv()
        
        # Setup logger early to log any issues
        self.logger = setup_logger(__name__)
        
        # Load configurations
        self.config = self._load_env_config()

        # Derive other paths from APP_ROOT
        self.config['MODEL_CACHE_DIR'] = os.path.join(
            self.config['APP_ROOT'],
            'modules',
            'Providers',
            'HuggingFace',
            'model_cache'
        )
        # Ensure the model_cache directory exists
        os.makedirs(self.config['MODEL_CACHE_DIR'], exist_ok=True)

        # Validate the API key for the default provider
        default_provider = self.config.get('DEFAULT_PROVIDER', 'OpenAI')
        if not self._is_api_key_set(default_provider):
            raise ValueError(f"{default_provider} API key not found in environment variables")

    def _load_env_config(self) -> Dict[str, Any]:
        """
        Loads environment variables into the configuration dictionary.

        Returns:
            Dict[str, Any]: A dictionary containing all loaded configuration settings.
        """
        config = {
            'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
            'DEFAULT_PROVIDER': os.getenv('DEFAULT_PROVIDER', 'OpenAI'),
            'DEFAULT_MODEL': os.getenv('DEFAULT_MODEL', 'gpt-4o'),
            'MISTRAL_API_KEY': os.getenv('MISTRAL_API_KEY'),
            'HUGGINGFACE_API_KEY': os.getenv('HUGGINGFACE_API_KEY'),
            'GOOGLE_API_KEY': os.getenv('GOOGLE_API_KEY'),
            'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY'),
            'GROK_API_KEY': os.getenv('GROK_API_KEY'),  
            'APP_ROOT': os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        }
        self.logger.info(f"APP_ROOT is set to: {config['APP_ROOT']}")
        return config

    def get_config(self, key: str, default: Any = None) -> Any:
        """
        Retrieves a configuration value by its key.

        Args:
            key (str): The configuration key to retrieve.
            default (Any, optional): The default value to return if the key is not found.

        Returns:
            Any: The value associated with the key, or the default value if key is absent.
        """
        return self.config.get(key, default)

    def get_model_cache_dir(self) -> str:
        """
        Retrieves the directory path where models are cached.

        Returns:
            str: The path to the model cache directory.
        """
        return self.get_config('MODEL_CACHE_DIR')

    def get_default_provider(self) -> str:
        """
        Retrieves the default provider name from the configuration.

        Returns:
            str: The name of the default provider.
        """
        return self.get_config('DEFAULT_PROVIDER')

    def get_default_model(self) -> str:
        """
        Retrieves the default model name from the configuration.

        Returns:
            str: The name of the default model.
        """
        return self.get_config('DEFAULT_MODEL')


    def get_openai_api_key(self) -> str:
        """
        Retrieves the OpenAI API key from the configuration.

        Returns:
            str: The OpenAI API key.
        """
        return self.get_config('OPENAI_API_KEY')

    def get_mistral_api_key(self) -> str:
        """
        Retrieves the Mistral API key from the configuration.

        Returns:
            str: The Mistral API key.
        """
        return self.get_config('MISTRAL_API_KEY')

    def get_huggingface_api_key(self) -> str:
        """
        Retrieves the HuggingFace API key from the configuration.

        Returns:
            str: The HuggingFace API key.
        """
        return self.get_config('HUGGINGFACE_API_KEY')

    def get_google_api_key(self) -> str:
        """
        Retrieves the Google API key from the configuration.

        Returns:
            str: The Google API key.
        """
        return self.get_config('GOOGLE_API_KEY')

    def get_anthropic_api_key(self) -> str:
        """
        Retrieves the Anthropic API key from the configuration.

        Returns:
            str: The Anthropic API key.
        """
        return self.get_config('ANTHROPIC_API_KEY')

    def get_grok_api_key(self) -> str:
        """
        Retrieves the Grok API key from the configuration.

        Returns:
            str: The Grok API key.
        """
        return self.get_config('GROK_API_KEY')

    def get_app_root(self) -> str:
        """
        Retrieves the application's root directory path.

        Returns:
            str: The path to the application's root directory.
        """
        return self.get_config('APP_ROOT')

    def update_api_key(self, provider_name: str, new_api_key: str):
        """
        Updates the API key for a specified provider in the .env file and reloads
        the environment variables to reflect the changes immediately.

        Args:
            provider_name (str): The name of the provider whose API key is to be updated.
            new_api_key (str): The new API key to set for the provider.

        Raises:
            FileNotFoundError: If the .env file is not found.
            ValueError: If the provider name does not have a corresponding API key mapping.
        """
        env_path = find_dotenv()
        if not env_path:
            raise FileNotFoundError("`.env` file not found.")

        provider_env_keys = {
            "OpenAI": "OPENAI_API_KEY",
            "Mistral": "MISTRAL_API_KEY",
            "Google": "GOOGLE_API_KEY",
            "HuggingFace": "HUGGINGFACE_API_KEY",
            "Anthropic": "ANTHROPIC_API_KEY",
            "Grok": "GROK_API_KEY",  
        }

        env_key = provider_env_keys.get(provider_name)
        if not env_key:
            raise ValueError(f"No API key mapping found for provider '{provider_name}'.")

        # Update the .env file
        set_key(env_path, env_key, new_api_key)
        self.logger.info(f"API key for {provider_name} updated successfully.")

        # Reload environment variables
        load_dotenv(env_path, override=True)
        self.config[env_key] = new_api_key

    def _is_api_key_set(self, provider_name: str) -> bool:
        """
        Checks if the API key for a specified provider is set.

        Args:
            provider_name (str): The name of the provider.

        Returns:
            bool: True if the API key is set, False otherwise.
        """
        api_key = self.get_config(f"{provider_name.upper()}_API_KEY")
        return bool(api_key)

    def get_available_providers(self) -> Dict[str, str]:
        """
        Retrieves a dictionary of available providers and their corresponding API keys.

        Returns:
            Dict[str, str]: A dictionary where keys are provider names and values are their API keys.
        """
        providers = ["OpenAI", "Mistral", "Google", "HuggingFace", "Anthropic", "Grok"]
        return {provider: self.get_config(f"{provider.upper()}_API_KEY") for provider in providers}
