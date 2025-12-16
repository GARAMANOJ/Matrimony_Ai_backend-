# In app/core/config.py

import os
from typing import Optional

class Settings:
    """
    A simple class to hold application settings.
    It reads directly from environment variables, which are injected by Docker Compose.
    """
    def __init__(self):
        # These will be loaded from the environment variables
        # that Docker Compose injects from your .env file.
        self.DATABASE_URL: str = os.getenv("DATABASE_URL")
        self.SECRET_KEY: str = os.getenv("SECRET_KEY")
        self.ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

        # Validate that critical variables are present
        if not self.DATABASE_URL or not self.SECRET_KEY:
            raise RuntimeError("DATABASE_URL or SECRET_KEY missing in environment. Check your .env file.")

# Create a single settings instance to be used throughout the application
settings = Settings()

print("✅ ENV LOADED")
print("DATABASE_URL =", settings.DATABASE_URL)