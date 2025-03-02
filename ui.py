import streamlit as st
import time
import os
import threading
from src import YouTubeScriptInput, YouTubeScriptGenerator

st.set_page_config(
    page_title="YouTube Script Generator", page_icon="🎬", layout="centered"
)


class YouTubeScriptApp:
    def __init__(self):
        self.script_generated = False
        self.yt_script_generator = YouTubeScriptGenerator()

    def run_generation(self, youtube_inputs):
        """Background function to run script generation."""
        self.yt_script_generator.generate(youtube_inputs)
        self.script_generated = True  # Mark process as completed

    def check_script_status(self):
        """Continuously check for each processing step in the background."""
        path = self.yt_script_generator.paths.base
        blueprint_done = search_done = refined_done = False

        while not self.script_generated:
            time.sleep(1)

            if not blueprint_done and os.path.exists(
                os.path.join(path, "blueprint.json")
            ):
                st.success("📜 Blueprint Done ✅")
                blueprint_done = True

            if not search_done and os.path.exists(
                os.path.join(path, "internet_search")
            ):
                if any(
                    f.endswith(".json")
                    for f in os.listdir(os.path.join(path, "internet_search"))
                ):
                    st.info("🔍 Internet Search Done ✅")
                    search_done = True

            if not refined_done and os.path.exists(
                os.path.join(path, "refined_blueprint.json")
            ):
                st.success("📜 Refined Outline Done ✅")
                refined_done = True

            if self.script_generated:
                break

    def read_file(self, filename):
        """Utility function to read the content of a file."""
        file_path = os.path.join(self.yt_script_generator.paths.base, filename)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        return "File not found!"

    def main(self):
        st.title("🎥 YouTube Script Generator")
        st.markdown("---")

        language = st.text_input("🌍 Language for the script:")
        tone = st.selectbox(
            "🎭 Tone:",
            [
                "Incorporate little Humor in the Video",
                "Present Only Facts",
                "Emotional",
                "Inspirational",
                "Educational",
                "Entertaining",
                "Custom",
            ],
        )
        if tone == "Custom":
            tone = st.text_input("📝 Enter custom tone:")

        video_length = st.selectbox(
            "⏳ Video Length:",
            [
                "TikTok/Shots/Reel (15-30 seconds)",
                "10-15 min short video",
                "20-30 min short video",
            ],
        )
        video_title = st.text_input("🎬 Video Title:")
        description = st.checkbox("Include Video Description")

        if st.button("🚀 Generate Script"):
            st.markdown("---")
            st.subheader("Your Selections:")
            st.write(f"**🌍 Language:** {language}")
            st.write(f"**🎭 Tone:** {tone}")
            st.write(f"**⏳ Video Length:** {video_length}")
            st.write(f"**🎬 Video Title:** {video_title}")

            youtube_inputs = YouTubeScriptInput(
                language=language,
                tone=tone,
                video_length=video_length,
                video_title=video_title,
                description=description,
            )
            with st.spinner("generating ..."):
                thread = threading.Thread(
                    target=self.run_generation, args=(youtube_inputs,)
                )
                thread.start()

                self.check_script_status()
                thread.join()

            script = self.read_file("script_output.txt")
            st.markdown("### 📝 Generated Script")
            st.markdown(script)

            if description:
                desc = self.read_file("video_description.txt")
                st.markdown("### 📝 Video Description")
                st.markdown(desc)

            st.success("✨ Script generation complete!")


if __name__ == "__main__":
    app = YouTubeScriptApp()
    app.main()
