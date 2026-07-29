import os
from config.settings import Settings

# Read from environment variables set during pytest initialization
env = os.getenv("TEST_ENV", "dev")
settings = Settings(env)

BASE_URL = settings.base_url
BROWSER = os.getenv("TEST_BROWSER", "chrome")
TIMEOUT = settings.timeout
