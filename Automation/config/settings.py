import os
from dotenv import load_dotenv


class Settings:

    def __init__(self, env="dev"):

        env_file = os.path.join(
            os.path.dirname(__file__),
            f".env.{env}"
        )

        load_dotenv(env_file, override=True)

        self.BASE_URL = os.getenv("BASE_URL")

        self.USERNAME = os.getenv("USERNAME")

        self.PASSWORD = os.getenv("PASSWORD")

        self.BROWSER = os.getenv("BROWSER")

        self.TIMEOUT = int(os.getenv("TIMEOUT", 10))