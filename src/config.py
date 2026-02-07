import os
from dotenv import load_dotenv

# Load the .env file immediately
load_dotenv()

class Config:
    API_KEY = os.getenv("HENRIK_API_KEY")
    NAME = os.getenv("VALORANT_NAME")
    TAG = os.getenv("VALORANT_TAG")
    REGION = "na"  # Defaulting to NA, can also be added to .env

    @classmethod
    def validate(cls):
        if not all([cls.API_KEY, cls.NAME, cls.TAG]):
            raise ValueError("Missing critical environment variables. Check .env file.")

# Validate on import to ensure integrity
Config.validate()