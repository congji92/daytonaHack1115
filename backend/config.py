"""
Configuration module - loads API keys from .env file

Simple and straightforward: just load environment variables and validate they exist.
"""

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# API Keys for sponsor services
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SENTRY_DSN = os.getenv("SENTRY_DSN")
GALILEO_API_KEY = os.getenv("GALILEO_API_KEY")
DAYTONA_API_KEY = os.getenv("DAYTONA_API_KEY")
DAYTONA_API_URL = os.getenv("DAYTONA_API_URL", "https://app.daytona.io/api")

def validate_config():
    """Validate that all required API keys are present."""
    missing = []

    if not OPENAI_API_KEY:
        missing.append("OPENAI_API_KEY")
    if not SENTRY_DSN:
        missing.append("SENTRY_DSN")
    if not GALILEO_API_KEY:
        missing.append("GALILEO_API_KEY")
    if not DAYTONA_API_KEY:
        missing.append("DAYTONA_API_KEY")

    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    return True
