import json

screen_w = 800
screen_h = 600
CONFIG_FILE_PATH = './configs/config.json'
DEBUG = False


def open_configs() -> dict:
    with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as config:
        return json.load(config)