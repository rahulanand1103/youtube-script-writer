import os
import json
from rich.console import Console
from rich.text import Text
from rich.logging import RichHandler
from typing import List, Dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.agent_prompt import GetPrompt
from src.baseLLM import BaseLLM


# Initialize Rich console
console = Console()


class GenerateScript(BaseLLM):
    def __init__(
        self,
        refine_output: str,
        model="gpt-4o",
    ) -> None:
        super().__init__(model)
        self.output_folders = refine_output
        self.k = 2

        blueprint_path = os.path.join(refine_output, "refined_blueprint.json")
        try:
            with open(blueprint_path, "r") as file:
                self.refine_blueprint = json.load(file)
            console.print(
                Text(
                    f"✅ Loaded refined blueprint from {blueprint_path}",
                    style="bold green",
                )
            )
        except Exception as e:
            console.print(
                Text(f"❌ Error loading blueprint: {str(e)}", style="bold red")
            )
            raise

    @staticmethod
    def _fetch_prompt() -> str:
        """Fetches the structured prompt for YouTube content strategy."""
        return GetPrompt.get_prompt("youtube_script_writer")

    def _get_section_prompt(self):
        """Generate the prompt for section writing."""
        writer_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self._fetch_prompt()),
                (
                    "user",
                    """
                    Video Title: {video_title}\n
                    Full Video Length: {video_length}\n
                    Tone: {tone}\n
                    Section Name: {section_name}\n
                    Allocated Time: {allocated_Time}\n
                    Internet Search: {internet_search}\n
                    Language: {language}\n
                    Guidance: {guidance}
                    """,
                ),
            ]
        )
        return writer_prompt

    def _generate_section(
        self, index: int, section: Dict, data: List[str], inputs
    ) -> str:
        """Generates content for a section."""
        section_name = section["section_title"]
        section_description = section["description"]
        section_time = section["time"]
        section_guidance = section["pointers"]

        console.print(
            Text(
                f"✍️ Generating content for section: {section_name}", style="bold yellow"
            )
        )

        writer_prompt = self._get_section_prompt()
        writer = writer_prompt | self.llm | StrOutputParser()

        complete_output = writer.invoke(
            {
                "video_title": inputs.video_title,
                "video_length": inputs.video_length,
                "tone": inputs.tone,
                "section_name": f"Title: {section_name}\nDescription: {section_description}",
                "allocated_Time": section_time,
                "internet_search": "\n".join(data),
                "language": inputs.language,
                "guidance": section_guidance,
            }
        )

        return complete_output

    def generate(self, inputs):
        """Main function to generate the entire script."""
        sections = self.refine_blueprint["sections"]
        complete_output = ""
        console.print(Text("🔄 Research Workflow Initialized", style="bold green"))
        for index, section in enumerate(sections):
            internet_search_path = os.path.join(
                self.output_folders, "internet_search", f"{index+1}.json"
            )
            try:
                with open(internet_search_path, "r") as file:
                    data = json.load(file)
                content = [x["content"] for x in data["internet_search"]]
            except Exception as e:
                console.print(
                    Text(
                        f"⚠️ Failed to load internet search data: {str(e)}",
                        style="bold red",
                    )
                )
                content = []

            section_output = self._generate_section(index, section, content, inputs)
            complete_output += f"\n#### Section: {section['section_title']}\n[{section['time']}]: {section_output}\n"


        output_file = os.path.join(self.output_folders, "script_output.txt")
        with open(output_file, "w") as file:
            file.write(complete_output)

        console.print(
            Text(f"✅ Script generated and saved to {output_file}", style="bold green")
        )
