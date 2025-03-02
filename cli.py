from rich.console import Console
from rich.table import Table
import questionary
from src import YouTubeScriptInput, YouTubeScriptGenerator


def get_youtube_script_input() -> YouTubeScriptInput:
    ## video title
    video_title = questionary.text("Enter video title:").ask()

    ## video length
    video_length = questionary.select(
        "Select video length:",
        choices=[
            "TikTok/Shots/Reel (15-30 seconds)",
            "10-15 min short video",
            "20-30 min short video",
        ],
    ).ask()

    language = questionary.text(
        "In which language would you like to generate your YouTube script (e.g., English or French)?"
    ).ask()

    tone = questionary.select(
        "Select video tone:",
        choices=[
            "Incorporate little Humor in the Video",
            "Present Only Facts",
            "Emotional",
            "Inspirational",
            "Educational",
            "Entertaining",
            "Customize Content Style",
        ],
    ).ask()

    if tone == "Customize Content Style":
        tone = questionary.text("Enter custom video type:").ask()

    generate_description = questionary.confirm(
        "Do you want to generate a video description?"
    ).ask()

    return YouTubeScriptInput(
        language=language,
        tone=tone,
        video_length=video_length,
        video_title=video_title,
        description=generate_description,
    )


def display_youtube_script_input(inputs: YouTubeScriptInput):
    console = Console()
    table = Table(title="Video Configuration")
    table.add_column("Field", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    table.add_row("Language", inputs.language)
    table.add_row("Video Type", inputs.tone)
    table.add_row("Video Length", inputs.video_length)
    table.add_row("Video Title", inputs.video_title)
    table.add_row("Generate Description", str(inputs.description))
    console.print(table)


if __name__ == "__main__":
    inputs = get_youtube_script_input()
    display_youtube_script_input(inputs)
    
    yt_script_generator = YouTubeScriptGenerator()
    yt_script_generator.generate(inputs)



