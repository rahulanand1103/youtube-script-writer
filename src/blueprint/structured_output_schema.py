from pydantic import BaseModel, Field
from typing import List, Optional


class Section(BaseModel):
    section_title: str = Field(..., title="Title of the section.Make sure the section title is meaningful.")
    description: str = Field(
        ...,
        title="Content of the section must be realted to youtube script. Don't add anything about video.",
    )
    time: str = Field(
        ...,
        title="Adjust the start and end times of this section based on the full video. For example, if the previous duration was [0-2 min], update it to [2-5 min] accordingly. Ensure the new timing aligns seamlessly with the overall flow of the video",
    )


class BluePrint(BaseModel):
    # Define the structure of the entire blueprint
    page_title: str = Field(..., title="Title of the page")
    sections: List[Section] = Field(
        default_factory=list,
        title="Title of the page. create a thought provoking and engaging Title/headline.",
    )
