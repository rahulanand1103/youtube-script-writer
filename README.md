# 🎥 YouTube Script Writer

<a href="https://www.producthunt.com/posts/youtube-script-writer?embed=true&utm_source=badge-featured&utm_medium=badge&utm_souce=badge-youtube&#0045;script&#0045;writer" target="_blank"><img src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=939465&theme=neutral&t=1741456962432" alt="youtube&#0032;script&#0032;writer - AI&#0045;powered&#0032;scripts&#0044;&#0032;tailored&#0032;for&#0032;your&#0032;YouTube&#0032;videos | Product Hunt" style="width: 250px; height: 54px;" width="250" height="54" /></a>

YouTube Script Writer is an open-source AI-agent that streamlines script generation for YouTube videos. By inputting a **<span style="color:#FF5733;">video title</span>**, **<span style="color:#33C3FF;">language</span>**, and **<span style="color:#28A745;">tone</span>** (e.g., *"Incorporate Humor," "Present Only Facts," "Emotional," "Inspirational"*), content creators can quickly generate tailored scripts.  

The tool adapts to various **<span style="color:#D63384;">video lengths</span>**, from **<span style="color:#FFC300;">short TikTok-style clips (15-30 seconds)</span>** to **<span style="color:#FF5733;">longer formats (10-30 minutes)</span>**, handling both research and writing so creators can focus on delivering their unique content.

**Example: Deepseek**: [Deepseek-Example](https://github.com/rahulanand1103/youtube-script-writer/tree/main/docs/sample%20script/deepseek)



## WHY YOUTUBE SCRIPT WRITER?  

- **📝 AI-Powered Scripts** – Generates structured, engaging scripts automatically.  
- **🌍 Smart Research** – Gathers accurate, real-time information.  
- **🧠 Context-Aware Writing** – Ensures logical flow and coherence.  
- **⚡ Fast & Efficient** – Speeds up content creation with minimal effort.   
- **📈 Scalable** – Suitable for solo creators and large teams.  

## Directory

```
.
├── scripts/                                  # Output folder for generated scripts  
├── src/                                      # Source code directory  
│   ├── agent_prompt/                         # Handles AI agent prompts  
│   │   ├── __init__.py  
│   │   ├── get_prompt.py                     # Retrieves specific agent prompts  
│   │   └── prompt.yaml                       # Stores all prompt templates  
│   ├── blueprint/                            # Generates initial script blueprints  
│   │   ├── __init__.py  
│   │   ├── create_blueprint.py               # Defines the script's initial structure  
│   │   └── structured_output_schema.py       # Defines schema for structured output  
│   ├── create_description/                   # Generates video descriptions  
│   │   ├── __init__.py  
│   │   └── create_description.py             # Creates and formats video descriptions  
│   ├── internet_research/                    # Conducts internet-based research  
│   │   ├── __init__.py  
│   │   └── researcher.py                     # Fetches and processes online data  
│   ├── refined_blueprint/                    # Refines blueprints based on research  
│   │   ├── __init__.py  
│   │   ├── refined_blueprint.py              # Enhances the initial blueprint  
│   │   └── structured_output_schema.py       # Defines refined output schema  
│   ├── writer/                               # Handles script writing  
│   │   ├── __init__.py  
│   │   └── writer.py                         # Generates final script text  
│   ├── __init__.py  
│   ├── main.py                               # Main execution script  
│   ├── datatypes.py                          # Defines custom data types  
├── LICENSE                                   # License information  
├── README.md                                 # Project documentation  
├── cli.py                                    # Command-line interface for running scripts  
├── requirements.txt                          # List of dependencies  
└── ui.py                                     # User interface module  

```


## 🎥 Demo
### UI
https://github.com/user-attachments/assets/b215ad58-58f9-42d7-922e-ec7fcfe916a5

### CLI
https://github.com/user-attachments/assets/53ab03ca-0d0d-4c83-9303-f2a74f13c85b


## 🏗️ Architecture
![Image](https://github.com/user-attachments/assets/f3f60ea2-536d-48b1-bea6-18b769997896)
YouTube Script Writer follows a structured approach to script generation:



### 📌 Steps:

1. **Create Initial Outline** - Generates a rough structure of the script.
2. **Perform Internet Research** - Collects relevant data from various sources.
3. **Refine Outline** - Improves the initial outline based on research findings.
4. **Write Each Section** - Generates detailed content for each section of the script.

## ⚙️ Getting Started

### Installation

1. Install Python 3.11 or later.
2. Clone the project and navigate to the directory:

    ```bash
    git clone https://github.com/rahulanand1103/youtube-script-writer.git
    cd youtube-script-writer
    ```

3. Set up API keys by exporting them or storing them in a `.env` file:

   ```bash
    export OPENAI_API_KEY={Your OpenAI API Key here}
    export YDC_API_KEY={Your API search key here, replacing <__> with \<_\__\> or put inside ""}
    ```
4. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Run the CLI or UI:

    - **Using the CLI:**

      ```bash
      python cli.py
      ```

    - **Using the Streamlit UI:**

      ```bash
      streamlit run ui.py
      ```

6. Open the UI in your browser:  

    ```
    http://localhost:8000
    ```

## 🐳 Running with Docker

You can run both the CLI and UI interfaces using Docker Compose without installing Python or dependencies directly on your system.

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed on your system.

### Setup

1. **To run only one of the services:**  
   Add your API keys in the command or use an `.env` file.

   ```bash
   # For UI only
   sudo OPENAI_API_KEY="your_openai_key" YDC_API_KEY="your_ydc_key" docker-compose up ui

   # For CLI only
   sudo OPENAI_API_KEY="your_openai_key" YDC_API_KEY="your_ydc_key" docker-compose up cli
   ```

