import os
import json
import requests
import hashlib
import time
import csv


def read_json_file(file_path: str) -> dict:
    with open(file_path) as json_file:
        return json.load(json_file)

def load_configuration_file(config_file_path: str) -> dict:
    return read_json_file(config_file_path)

def to_md5(value: str) -> str:
    return hashlib.md5(value.encode('utf-8')).hexdigest()

def cache_file(cache_name: str):
    return f'.cache/{cache_name}.json'

def cache_exist(cache_name: str) -> bool:
    return os.path.isfile(cache_file(cache_name))

def is_cache_fresh(cache_name: str) -> bool:
    return (os.path.getmtime(cache_file(cache_name)) + 24 * 60 * 60) > time.time()

def cache_exist_and_is_fresh(cache_name) -> bool:
    return cache_exist(cache_name) and is_cache_fresh(cache_name)

def read_cache_file(cache_name: str) -> bool:
    print('Reading from cache:', cache_name)
    return read_json_file(cache_file(cache_name))

def execute_request(url: str) -> str:
    print('Online request:', url)
    return requests.get(url).json()

def save_cache(cache_name: str, content: str):
    with open(cache_file(cache_name), 'w') as file:
        json.dump(content, file)

def pass_and_save_response(url: str, cache_name: str) -> str:
    result = execute_request(url)
    save_cache(cache_name, result)
    return result
    
def get_data(url: str) -> str:
    cache_name = to_md5(url)
    return read_cache_file(cache_name) if cache_exist_and_is_fresh(cache_name) else pass_and_save_response(url, cache_name)

def api_get_own_games(steam_api_key: str):
    return lambda steam_user_id: f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={steam_api_key}&steamid={steam_user_id}&format=json&include_appinfo=true'

def get_only_games_data(steam_games):
    return steam_games['response']['games']

settings = load_configuration_file('settings.json')
games = get_only_games_data(get_data(api_get_own_games(settings['steam']['api_key'])(settings['steam']['user_id'])))
game = games[0]
print(game)
