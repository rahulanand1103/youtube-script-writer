import os
import json
from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate
from src.blueprint.structured_output_schema import BluePrint
from src.agent_prompt import GetPrompt
from rich.console import Console
from rich.logging import RichHandler
import logging
from src.baseLLM import BaseLLM

# Initialize Rich Console
console = Console()

# Configure logging with Rich
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, markup=True)],  # Enables colored logs
)
logger = logging.getLogger("rich")


class CreateBlueprint(BaseLLM):
    def __init__(self, output_folder: str, model: str = "gpt-4o"):
        """Initializes the CreateBlueprint class with model and output folder settings."""
        super().__init__(model)
        self.output_folder = Path(output_folder)

    @staticmethod
    def _fetch_prompt() -> str:
        """Fetches the structured prompt for YouTube content strategy."""
        return GetPrompt.get_prompt("youtube_content_strategist")

    def _build_prompt_template(self) -> ChatPromptTemplate:
        """Builds a structured prompt template for the LLM."""
        return ChatPromptTemplate.from_messages(
            [
                ("system", self._fetch_prompt()),
                (
                    "user",
                    "Video Title: {video_title}\nVideo Length: {video_length}",
                ),
            ]
        )

    def generate(self, inputs) -> dict:
        """
        Generates a blueprint for YouTube content strategy using the LLM.

        :param inputs: An object containing `video_title`, `tone`, and `video_length`
        :return: Dictionary containing the structured output.
        """
        blueprint_prompt = self._build_prompt_template()
        generate_blueprint_direct = blueprint_prompt | self.llm.with_structured_output(
            BluePrint
        )

        try:
            output = generate_blueprint_direct.invoke(
                {
                    "video_title": inputs.video_title,
                    "video_length": inputs.video_length,
                }
            )
            console.print(
                "[bold cyan]✔ Blueprint generated successfully![/bold cyan]"
            )  # Colored output
        except Exception as e:
            logger.error(f"[bold red]❌ Error during LLM invocation:[/bold red] {e}")
            raise

        self._save_blueprint(output.dict())
        return output.dict()

    def _save_blueprint(self, data: dict) -> None:
        """Saves the generated blueprint to a JSON file."""
        self.output_folder.mkdir(parents=True, exist_ok=True)
        file_path = self.output_folder / "blueprint.json"

        with file_path.open("w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4)

        console.print(
            f"[bold green]✔ Blueprint saved successfully at:[/bold green] {file_path}"
        )
