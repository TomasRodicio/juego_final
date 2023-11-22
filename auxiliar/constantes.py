import json

screen_w = 1600
screen_h = 900
CONFIG_FILE_PATH = './configs/config.json'
DEBUG = False


def open_configs() -> dict:
    with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as config:
        return json.load(config)