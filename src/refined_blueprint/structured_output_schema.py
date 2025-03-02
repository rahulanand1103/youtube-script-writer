from typing import List, Optional
from pydantic import BaseModel, Field


class Section(BaseModel):
    section_title: str = Field(
        ...,
        title="Title of the section.Make sure the section title is meaningful,Engaging and must be based upon research.",
    )
    description: str = Field(
        ...,
        title="Content of the section must be realted to youtube script. Don't add anything about video.",
    )
    time: str = Field(..., title="starting and end of this section")

    pointers: str = Field(
        description="Provide clear guidance in pointer on what the writer should cover in this section based upon search to ensure engaging and informative content"
    )

    @property
    def as_str(self) -> str:
        return f"## {self.section_title}\n\n{self.description}".strip()


class RefinedBluePrint(BaseModel):
    page_title: str = Field(
        ...,
        title="Title of the video.",
    )
    sections: List[Section] = Field(
        default_factory=list,
        title="Titles and descriptions for each section of the video.",
    )
