import os
import json
import logging
from typing import List, Dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import chain
from src.refined_blueprint.structured_output_schema import RefinedBluePrint
from src.agent_prompt import GetPrompt
from rich.console import Console
from src.baseLLM import BaseLLM

# Initialize Rich Console
console = Console()


class YouTubeScriptArchitect(BaseLLM):
    def __init__(
        self,
        base_path: str,
        uuid: str,
        model="gpt-4o",
    ):
        super().__init__(model)
        self.path = base_path
        self.uuid = uuid

    @staticmethod
    def _fetch_prompt() -> str:
        """Fetches the structured prompt for YouTube content strategy."""
        return GetPrompt.get_prompt("youtube_script_architect")

    def _get_prompt(self) -> ChatPromptTemplate:
        """Creates a ChatPromptTemplate for refining the YouTube script blueprint."""
        messages = [
            ("system", self._fetch_prompt()),
            (
                "user",
                (
                    """
                    Create and refine the YouTube script blueprint based on the following details:
                    
                    Video Title: {video_title}
                    Video Length: {video_length}
                    Old Blueprint: {initial_blueprint}
                    
                    Internet Search: {internet_research}
                    
                    Generate the refined YouTube script blueprint.
                    """
                ),
            ),
        ]
        return ChatPromptTemplate.from_messages(messages)

    def _get_internet_research(self, folder_path: str) -> str:
        """Reads all JSON files in a folder and extracts internet search content."""
        try:
            json_files = [f for f in os.listdir(folder_path) if f.endswith(".json")]
            internet_search_content = ""

            for file in json_files:
                file_path = os.path.join(folder_path, file)
                with open(file_path, "r") as f:
                    data = json.load(f)
                    section_title = data.get("section_info", {}).get(
                        "section_title", "Unknown Section"
                    )
                    internet_search_text = "\n".join(
                        [x["content"] for x in data.get("internet_search", [])]
                    )

                    internet_search_content += (
                        f"Section Title: {section_title}\n{internet_search_text}\n\n"
                    )

            return internet_search_content
        except Exception as e:
            logging.error(f"Error reading JSON files from {folder_path}: {str(e)}")
            return ""

    def _get_intial_blueprint(self, initial_blueprint: Dict) -> str:
        """Formats the initial blueprint as a string."""
        try:
            sections = [
                f"\nTitle: {section['section_title']}\nDescription: {section['description']}\nTime: {section['time']}"
                for section in initial_blueprint.get("sections", [])
            ]
            return (
                f"Video Title: {initial_blueprint.get('page_title', 'Unknown Title')}\n"
                + "".join(sections)
            )
        except Exception as e:
            logging.error(f"Error formatting initial blueprint: {str(e)}")
            return ""

    def refine_blueprint_run(self, inputs, initial_blueprint):
        """Runs the refinement process for the YouTube script blueprint."""
        try:
            initial_blueprint_str = self._get_intial_blueprint(initial_blueprint)
            internet_research = self._get_internet_research(self.path.internet_search)
            refine_blueprint_prompt = self._get_prompt()
            refine_blueprint_chain = (
                refine_blueprint_prompt
                | self.llm.with_structured_output(RefinedBluePrint)
            )

            refined_blueprint = refine_blueprint_chain.invoke(
                {
                    "video_title": inputs.video_title,
                    "video_length": inputs.video_length,
                    "initial_blueprint": initial_blueprint_str,
                    "internet_research": internet_research,
                }
            )

            output_file = os.path.join(self.path.base, "refined_blueprint.json")
            with open(output_file, "w") as json_file:
                json.dump(refined_blueprint.dict(), json_file, indent=4)
            console.print(
                f"[bold green]✔ Refined Blueprint saved successfully at:[/bold green] {output_file}"
            )
            return {"refined_output": refined_blueprint.dict()}
        except Exception as e:
            logging.error(f"Failed to refine blueprint: {str(e)}")
            return {"refined_output": None}
