import os
import json
from pathlib import Path
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import AnyMessage, add_messages
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, StateGraph
from rich.console import Console
from rich.logging import RichHandler
import logging
from langchain_community.tools.you import YouSearchTool
from langchain_community.utilities.you import YouSearchAPIWrapper

from src.agent_prompt import GetPrompt
from src.baseLLM import BaseLLM


# Setup Rich Console & Logging
console = Console()

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, markup=True)],
)
logger = logging.getLogger("rich")


## Graph state definition
class GraphState(TypedDict):
    topic: str
    questions: list
    internet_search: list
    topicid: str
    iterations: int
    section_info: dict
    summary: str


class Researcher(BaseLLM):
    def __init__(
        self,
        output_folder: str,
        model="gpt-4o",
        temperature=0.3,
        no_generate_question: int = 3,
        no_internet_results: int = 2,
    ):
        """Initialize the Researcher with LLM and output settings."""
        super().__init__(model)
        self.output_folder = Path(output_folder)
        self.state = None
        self.no_generate_question = no_generate_question
        self.no_internet_results = no_internet_results

    @staticmethod
    def _fetch_prompt() -> str:
        """Fetches the structured prompt for YouTube content strategy."""
        return GetPrompt.get_prompt("research_analyst")

    def _generate_question(self, state: GraphState) -> GraphState:
        """Generates a new question based on the given state."""
        console.print("[bold cyan]🔍 Generating question...[/bold cyan]")

        gen_qn_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self._fetch_prompt()),
                (
                    "user",
                    "Section Details: {section_details}\n Previously Generated Questions: {previous_questions}",
                ),
            ]
        )

        gen_qn_agent = gen_qn_prompt | self.llm
        section_details = (
            f'Section title: "{state["section_info"]["section_title"]}"\n'
            f'Section description: "{state["section_info"]["description"]}"'
        )

        previous_questions_string = (
            " ".join(
                [f"Q{index}: {str(q)}" for index, q in enumerate(state["questions"])]
            )
            if state["questions"]
            else "None"
        )

        try:
            generated_output = gen_qn_agent.invoke(
                {
                    "section_details": section_details,
                    "previous_questions": previous_questions_string,
                }
            ).content
            state["questions"].append(generated_output)

            console.print(
                f"[bold green]✅ Generated Question:[/bold green] {generated_output}"
            )
        except Exception as e:
            logger.error(f"[bold red]❌ Error generating question:[/bold red] {e}")
            raise

        return state

    def _internet_search(self, state: GraphState) -> GraphState:
        """Performs an internet search using the latest generated question."""
        console.print("[bold cyan]🌍 Performing Internet Search...[/bold cyan]")

        try:
            api_wrapper = YouSearchAPIWrapper(num_web_results=self.no_internet_results)
            youTool = YouSearchTool(api_wrapper=api_wrapper)
            results = youTool.run(state["questions"][-1])

            for index, result in enumerate(results):
                search_data = {
                    "content": result.page_content,
                    "url": result.metadata["url"],
                    "title": result.metadata["title"],
                }
                state["internet_search"].append(search_data)

        except Exception as e:
            logger.error(f"[bold red]❌ Internet search failed:[/bold red] {e}")
            raise

        return state

    def _save_data(self, state: GraphState) -> None:
        """Saves the collected research data to a JSON file."""
        self.output_folder.mkdir(parents=True, exist_ok=True)
        file_path = (
            self.output_folder / "internet_search" / f"{state['iterations']}.json"
        )
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with file_path.open("w", encoding="utf-8") as json_file:
            json.dump(state, json_file, indent=4)

        console.print(
            f"[bold green]💾 Research data saved at:[/bold green] {file_path}"
        )

    def end_flow_decision(self, state: GraphState) -> str:
        """Determines whether to continue or end the research process."""
        if len(state["questions"]) >= self.no_generate_question:
            self._save_data(state)
            return "end"
        else:
            return "continue"

    def run(self, initial_state: GraphState) -> GraphState:
        """Runs the research workflow using a state graph."""
        console.print("[bold cyan]🚀 Starting Research Process...[/bold cyan]")

        workflow = StateGraph(GraphState)
        workflow.add_node("generate_question", self._generate_question)
        workflow.add_node("search_internet", self._internet_search)

        workflow.set_entry_point("generate_question")
        workflow.add_edge("generate_question", "search_internet")
        workflow.add_conditional_edges(
            "search_internet",
            self.end_flow_decision,
            {
                "end": END,
                "continue": "generate_question",
            },
        )

        app = workflow.compile()

        console.print("[bold green]🔄 Research Workflow Initialized[/bold green]")
        return app.invoke(initial_state)
