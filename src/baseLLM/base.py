import os
import logging
from rich.logging import RichHandler
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
# Configure logging with RichHandler
logging.basicConfig(
    level=logging.INFO, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)

logger = logging.getLogger(__name__)


class BaseLLM:
    def __init__(self, model: str):
        """Base class for initializing an LLM."""
        self.llm = self._initialize_llm(model)

    @staticmethod
    def _initialize_llm(model: str) -> ChatOpenAI:
        """Initializes the ChatOpenAI model."""
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            logger.error(
                "[bold red]❌ OPENAI_API_KEY is not set in environment variables.[/bold red]"
            )
            raise ValueError("Missing OPENAI_API_KEY. Please set it in your .env file.")

        logger.info(f"[bold green]✅ Loaded OpenAI Model:[/bold green] {model}")
        return ChatOpenAI(model=model)
