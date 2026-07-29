import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self, env="dev"):
        self.env = env.lower()
        self.base_url = self._get_base_url()
        self.timeout = int(os.getenv("TIMEOUT", "10"))

    def _get_base_url(self):
        env_urls = {
            "dev": "http://127.0.0.1:8000/",
            "qa": "http://qa.smartwaste.local/",
            "staging": "http://staging.smartwaste.local/",
            "prod": "https://smartwaste.community/"
        }
        # Allow overriding via environment variable, or fallback to standard env maps
        return os.getenv("BASE_URL") or env_urls.get(self.env, "http://127.0.0.1:8000/")
