import os
import logging
from dotenv import load_dotenv
from rich.logging import RichHandler

# Configure logging with Rich
logging.basicConfig(level=logging.ERROR, handlers=[RichHandler()])
logger = logging.getLogger(__name__)

class APIKeyManager:
    """Manages API keys by checking existing environment variables first, then falling back to .env file."""

    REQUIRED_KEYS = ["OPENAI_API_KEY", "YDC_API_KEY"]

    @classmethod
    def load_and_validate_keys(cls) -> bool:
        """Ensure required API keys are set, preferring system environment variables over .env file.
        
        Returns:
            bool: True if all keys are set, False if any key is missing.
        """
        
        # Load .env file (if needed)
        load_dotenv()

        missing_keys = []

        for key in cls.REQUIRED_KEYS:
            env_value = os.environ.get(key)  # Check if key is set via `export`
            dotenv_value = os.getenv(key)    # Check if key exists in .env

            # Ensure the key is not empty and strip whitespace
            if env_value and env_value.strip():
                os.environ[key] = env_value.strip()  # Keep already set system env variable
            elif dotenv_value and dotenv_value.strip():
                os.environ[key] = dotenv_value.strip()  # Set from .env if system env is missing
            else:
                missing_keys.append(key) 

        if missing_keys:
            logger.error(f"❌ Missing API keys: {', '.join(missing_keys)} | Set them using `export {missing_keys[0]}=your_api_key` or add them in `.env`")
            return False 

        logger.info("✅ All API keys are properly set.")
        return True  



