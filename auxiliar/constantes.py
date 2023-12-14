import json

screen_w = 1600
screen_h = 800
tile_size = 50
enemy_range = 1000
CONFIG_FILE_PATH = './configs/config.json'
DEBUG = False


def open_configs() -> dict:
    with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as config:
        return json.load(config)