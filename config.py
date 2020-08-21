from configparser import ConfigParser
from pathlib import Path


class Config:
    def __init__(self, config: ConfigParser):
        self.output_path: Path = Path(config['main']['path'])  # Куда сохранять результат?
        self.tokens: Path = Path(config['vk']['tokens'])  # Путь к файлу с токенами
        self.ids: Path = Path(config['main']['ids'])  # Путь к файлу с айдишниками, за которыми нужно следить


config_parser = ConfigParser()
config_parser.read('config.ini')

config = Config(config_parser)
