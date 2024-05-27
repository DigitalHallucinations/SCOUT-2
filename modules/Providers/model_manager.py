# modules/Providers/OpenAI/model_manager.py

class ModelManager:
    def __init__(self):
        self.MODEL = "gpt-4o"
        self.MAX_TOKENS = 4000
        self.ALLOWED_MODELS = [
            "gpt-3.5-turbo-1106", "gpt-4-0613", "gpt-3.5-turbo-16k-0613", 
            "gpt-3.5-turbo-0613", "gpt-4-1106-preview", "gpt-4-turbo-preview", 
            "gpt-4o", "gpt-4o-2024-05-13"
        ]

    def set_model(self, model_name):
        self.MODEL = model_name
        if self.MODEL in ["gpt-3.5-turbo-16k-0613", "gpt-3.5-turbo-16k"]:
            self.MAX_TOKENS = 4000
        elif self.MODEL in ["gpt-4-0613", "gpt-4", "gpt-4o", "gpt-4o-2024-05-13"]:
            self.MAX_TOKENS = 4000
        else:
            self.MAX_TOKENS = 2000

    def get_model(self):
        return self.MODEL

    def is_model_allowed(self):
        return self.MODEL in self.ALLOWED_MODELS

    def get_max_tokens(self):
        return self.MAX_TOKENS