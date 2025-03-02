from dataclasses import dataclass
from pathlib import Path


@dataclass
class YouTubeScriptInput:
    language: str
    tone: str
    video_length: str
    video_title: str
    description: bool


@dataclass
class ScriptPaths:
    base: Path
    internet_search: Path

    @classmethod
    def from_base(cls, base_path: Path):
        return cls(
            base=base_path,
            internet_search=base_path / "internet_search",
        )
