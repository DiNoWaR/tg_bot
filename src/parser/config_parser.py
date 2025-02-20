from src.model.bot_config import BotConfig
from pathlib import Path


class ConfigParser:
    def __init__(self):
        root_dir = Path(__file__).resolve().parents[2]
        self.path = f'{root_dir}/resources/config.json'

    def parse_config(self):
        with open(self.path, "r", encoding="utf-8") as file:
            json_data = file.read()
            return BotConfig.from_json(json_data)
