import os
import json
import requests
import hashlib
import time
import csv
import functools


def compose(*functions):
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions)

def trace(label):
    def internal(value):
        print(f'{label}: {value}')
        return value

    return internal

def get_all_keys(collection: list) -> list:

    def internal(prev, current):
        prev.update(current.keys())
        return prev

    return functools.reduce(internal, collection, set())

def read_json_file(file_path: str) -> dict:
    with open(file_path) as json_file:
        return json.load(json_file)

def load_configuration_file(config_file_path: str) -> dict:
    return read_json_file(config_file_path)

def to_md5(value: str) -> str:
    return hashlib.md5(value.encode('utf-8')).hexdigest()

def cache_exist(cache_file: str) -> bool:
    return os.path.isfile(cache_file)

def is_cache_fresh(cache_file: str) -> bool:
    return (os.path.getmtime(cache_file) + 24 * 60 * 60) > time.time()

def cache_exist_and_is_fresh(cache_file) -> bool:
    return cache_exist(cache_file) and is_cache_fresh(cache_file)

def read_cache_file(cache_file: str) -> bool:
    print('Reading from cache:', cache_file)
    return read_json_file(cache_file)

def execute_request(url: str) -> str:
    print('Online request:', url)
    return requests.get(url).json()

def save_cache(cache_file: str, content: str):
    with open(cache_file, 'w') as file:
        json.dump(content, file)

def pass_and_save_response(url: str, cache_file: str) -> str:
    result = execute_request(url)
    save_cache(cache_file, result)
    return result

def to_cache_file(cache_name: str) -> str:
    return f'.cache/{cache_name}.json'

def get_data(url: str) -> str:
    cache_file = to_cache_file(to_md5(url))
    return read_cache_file(cache_file) if cache_exist_and_is_fresh(cache_file) else pass_and_save_response(url, cache_file)

def api_get_own_games(steam_settings: str) -> str:
    steam_api_key = steam_settings['api_key']
    steam_user_id = steam_settings['user_id']

    return f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={steam_api_key}&steamid={steam_user_id}&format=json&include_appinfo=true'

def get_only_games_data(steam_games: dict) -> [dict]:
    return steam_games['response']['games']

def is_game(game: dict) -> bool:
    return game['img_icon_url']

def only_games(games: []) -> []:
    return filter(is_game, games)

def compact_steam_game_data(game: dict) -> dict:
    return {
        'DRM': 'Steam',
        'appid': game.get('appid', None),
        'name': game.get('name', None),
        'play_time': game.get('playtime_forever', 0)
    }

def compact_steam_games_data(games: list) -> list:
    return map(compact_steam_game_data, games)

get_games_from_steam = compose(compact_steam_games_data, only_games, get_only_games_data, get_data, api_get_own_games)

settings = load_configuration_file('settings.json')
with open('steam_library.csv', 'w', newline='') as csvfile:
    steam_game_keys = ['DRM', 'appid', 'name', 'play_time']
    writer = csv.DictWriter(csvfile, fieldnames=steam_game_keys)
    writer.writeheader()
    writer.writerows(get_games_from_steam(settings['steam']))
    csvfile.close()
