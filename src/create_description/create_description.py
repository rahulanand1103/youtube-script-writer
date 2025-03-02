import os
import logging
from pathlib import Path
from rich.console import Console
from rich.logging import RichHandler
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.agent_prompt import GetPrompt
from src.baseLLM import BaseLLM


# Initialize Rich Console
console = Console()

# Configure logging with Rich
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, markup=True)],
)
logger = logging.getLogger("rich")


class CreateDescription(BaseLLM):
    def __init__(self, model: str = "gpt-4o") -> None:
        """Initializes the CreateDescription class with model settings."""
        super().__init__(model)
        self.prompt_template = self._build_prompt_template()

    @staticmethod
    def _fetch_prompt() -> str:
        """Fetches the structured prompt for YouTube description writing."""
        return GetPrompt.get_prompt("youtube_description_writer")

    def _build_prompt_template(self) -> ChatPromptTemplate:
        """Builds a structured prompt template for the LLM."""
        return ChatPromptTemplate.from_messages(
            [
                ("system", self._fetch_prompt()),
                ("user", "Script Outline: {script_outline}"),
            ]
        )

    def generate_conclusion(self, script_outline: list) -> str:
        """Generates a conclusion based on the provided refined blueprint."""
        try:
            script_outline = "\n\n".join(script_outline)
            writer = self.prompt_template | self.llm | StrOutputParser()
            conclusion_output = writer.invoke({"script_outline": script_outline})
            console.print("[bold cyan]✔ Conclusion generated successfully![/bold cyan]")
            return conclusion_output
        except Exception as e:
            logger.error(f"[bold red]❌ Error generating conclusion:[/bold red] {e}")
            return ""
