import yaml


class GetPrompt:
    _prompt_cache = None

    @classmethod
    def _load_prompt(cls):
        if cls._prompt_cache is None:  # Load YAML only once
            with open("src/agent_prompt/prompt.yaml", "r", encoding="utf-8") as file:
                cls._prompt_cache = yaml.safe_load(file)

    @classmethod
    def get_prompt(cls, agent_name: str):
        cls._load_prompt()  # Ensure the YAML file is loaded
        return cls._prompt_cache.get(agent_name, {}).get("prompt", "")
