# modules/Providers/HuggingFace/utils/cache_manager.py

import os
import hashlib
import json
from typing import List, Dict

class CacheManager:
    def __init__(self, cache_file: str):
        self.cache_file = cache_file
        self.cache = self._load_cache()

    def _load_cache(self) -> Dict[str, str]:
        if not os.path.exists(self.cache_file):
            return {}
        try:
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def save_cache(self):
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)

    def get(self, key: str) -> str:
        return self.cache.get(key)

    def set(self, key: str, value: str):
        self.cache[key] = value
        self.save_cache()

    def generate_cache_key(self, messages: List[Dict[str, str]], model: str, settings: Dict) -> str:
        cache_data = json.dumps({"messages": messages, "model": model, "settings": settings})
        return hashlib.md5(cache_data.encode()).hexdigest()
