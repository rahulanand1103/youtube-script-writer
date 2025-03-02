import os
import uuid
from pathlib import Path
from rich.console import Console
from src.datatypes import YouTubeScriptInput, ScriptPaths


console = Console()
import json
from src.blueprint import CreateBlueprint
from src.internet_research import Researcher, GraphState
from src.refined_blueprint import YouTubeScriptArchitect
from src.writer import GenerateScript
from src.create_description import CreateDescription
from typing_extensions import TypedDict

from dataclasses import dataclass
from pathlib import Path
import uuid
from rich.console import Console
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.graph import END, StateGraph
from src.key_manager import APIKeyManager

console = Console()


class MainGraphState(TypedDict):
    paths: ScriptPaths
    script_uuid: str
    inputs: YouTubeScriptInput
    intial_blueprint: dict
    refined_blueprint: dict


class YouTubeScriptGenerator:
    def __init__(self, path: str = "scripts") -> None:
        self.script_uuid: str = str(uuid.uuid4())[:6]
        self.output_folder: Path = Path(path)
        self.paths: ScriptPaths = ScriptPaths.from_base(
            self.output_folder / self.script_uuid
        )

    def create_directory(self, main_state: MainGraphState) -> MainGraphState:
        """Creates a directory structure for the script."""

        if main_state["paths"].base.exists():
            console.print(
                f"[bold yellow]Directory \"{main_state['paths'].base}\" already exists.[/bold yellow]"

            )
            
            return

        for directory in [
            main_state["paths"].base,
            main_state["paths"].internet_search,
        ]:
            directory.mkdir(parents=True, exist_ok=True)
            console.print(
                f"[bold green]Directory '{directory}' created successfully![/bold green]"
            )
        return main_state

    def youtube_content_strategist(self, main_state: MainGraphState) -> MainGraphState:
        """
        ## Agent: youtube_content_strategist
        ## Task: is to create initial blueprint

        Args:
            inputs: (YouTubeScriptInput)
            output: bool
        """
        initial_blueprint = CreateBlueprint(main_state["paths"].base)
        intial_blueprint = initial_blueprint.generate(main_state["inputs"])
        main_state["intial_blueprint"] = intial_blueprint
        return main_state

    def research_analyst(self, main_state: MainGraphState) -> MainGraphState:
        """## Agent: research_analyst
           ## Task: is to do internet research

        Args:
            inputs (YouTubeScriptInput): _description_

        Returns:
            bool: _description_
        """
        for index, section in enumerate(main_state["intial_blueprint"]["sections"]):
            initial_state = GraphState(
                topic=main_state["intial_blueprint"]["page_title"],
                iterations=index + 1,
                section_info=section,
                questions=[],
                internet_search=[],
            )

            wiki_expert_dialogue = Researcher(main_state["paths"].base)
            wiki_expert_dialogue.run(initial_state=initial_state)
        return main_state

    def youtube_script_architect(self, main_state: MainGraphState) -> MainGraphState:
        YouTubeScriptArchitect(
            main_state["paths"], main_state["script_uuid"]
        ).refine_blueprint_run(main_state["inputs"], main_state["intial_blueprint"])
        return main_state

    def youtube_script_writer(self, main_state: MainGraphState) -> MainGraphState:
        generatearticle_obj = GenerateScript(refine_output=main_state["paths"].base)
        generatearticle_obj.generate(main_state["inputs"])
        return main_state

    def create_description(self, main_state: MainGraphState) -> MainGraphState:
        if main_state["inputs"].description:
            return "continue"
        else:
            return "end"

    def youtube_description_writer(self, main_state: MainGraphState):
        with open(f"{main_state['paths'].base}/refined_blueprint.json", "r") as file:
            refine_blueprint = json.load(file)

        refined_blueprint = f"Video Title: {refine_blueprint['page_title']}\n"

        for section in refine_blueprint["sections"]:
            refined_blueprint += (
                f"\nSection Name: {section['section_title']}\n"
                f"Section Description: {section['description']}\n"
                f"Time of this section: {section['time']}"
            )
        video_description = CreateDescription().generate_conclusion(refined_blueprint)
        print(video_description)

        with open(f"{self.paths.base}/video_description.txt", "w") as file:
            file.write(video_description)

    def generate(self, inputs: YouTubeScriptInput):
        if APIKeyManager.load_and_validate_keys():
            print("✅ API keys are validated and set.")
        else:
            print("❌ Some API keys are missing. Please set them as instructed above.")
        """Generates a new script with a unique ID."""
        main_state = MainGraphState(
            paths=self.paths,
            script_uuid=self.script_uuid,
            inputs=inputs,
            intial_blueprint=None,
            refined_blueprint=None,
        )

        workflow = StateGraph(MainGraphState)
        ## define all nodes
        workflow.add_node("create_directory", self.create_directory)
        workflow.add_node("youtube_content_strategist", self.youtube_content_strategist)
        workflow.add_node("research_analyst", self.research_analyst)
        workflow.add_node("youtube_script_architect", self.youtube_script_architect)
        workflow.add_node("youtube_script_writer", self.youtube_script_writer)
        workflow.add_node("youtube_description_writer", self.youtube_description_writer)
        ## creating edges
        workflow.add_edge("create_directory", "youtube_content_strategist")
        workflow.add_edge("youtube_content_strategist", "research_analyst")
        workflow.add_edge("research_analyst", "youtube_script_architect")
        workflow.add_edge("youtube_script_architect", "youtube_script_writer")
        workflow.add_conditional_edges(
            "youtube_script_writer",
            self.create_description,
            {
                "end": END,
                "continue": "youtube_description_writer",
            },
        )
        ## set-entry point
        workflow.set_entry_point("create_directory")
        ## complile
        app = workflow.compile()
        ## invoke
        app.invoke(main_state)


