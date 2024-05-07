import datetime
import json
import os
import re


def get_config() -> dict:
    rules = json.load(open("bot/config.json", 'r'))
    return rules


def get_rule(section: str, key: str):
    return get_config()[section][key]


def write_rule(section: str, key: str, value):
    rules = get_config()
    rules[section][key] = value
    json.dump(rules, open(get_rule('PATHS', 'CONFIG'), 'w'))
    return rules


def get_now(need_date: bool = True, need_date_only: bool = False):
    now = datetime.datetime.now()
    if need_date_only:
        return now.strftime("%d/%m/%Y")
    if need_date:
        return now.strftime("%d/%m/%Y %H:%M:%S")
    return now.strftime("%H:%M:%S")


def is_allowed_string(s: str, allowed_string: str):
    allowed_chars = set(allowed_string)
    return set(s).issubset(allowed_chars)


def uri_validator(url: str) -> bool:
    patterns = [
        r'^https://steamcommunity\.com/profiles/[0-9]+/$',
        r'^https://steamcommunity\.com/id/.+/$',
        r'^https://steamcommunity\.com/profiles/[0-9]+$',
        r'^http://steamcommunity\.com/profiles/[0-9]+/$',
        r'^http://steamcommunity\.com/id/.+/$',
        r'^http://steamcommunity\.com/profiles/[0-9]+$'
    ]

    if any(re.match(pattern, url) for pattern in patterns):
        return True
    return False


def write_users(data: dict):
    with open(get_rule('PATHS', 'USERS'), 'w', encoding='utf-8') as file:
        json.dump(data, file)


def get_users() -> dict:
    with open(get_rule('PATHS', 'USERS'), 'r', encoding='utf-8') as file:
        content = file.read()
        unpacked_data = json.loads(content)
    return unpacked_data


def get_latest_log_file(logs_directory: str = 'logs') -> str:
    # Получаем список всех файлов в директории logs
    log_files = [f for f in os.listdir(logs_directory) if f.startswith('log_') and f.endswith('.txt')]

    # Преобразуем имена файлов в формат datetime и сортируем
    log_files.sort(key=lambda x: datetime.datetime.strptime(x, 'log_%d%m%Y_%H%M%S.txt'), reverse=True)

    # Возвращаем самый новый файл
    return logs_directory + '/' + log_files[0] if log_files else None


def write_stats(data: dict):
    with open(get_rule('PATHS', 'STATS'), 'w', encoding='utf-8') as file:
        json.dump(data, file)
        print(f'[{get_now()}] Written stats.json')


def get_stats() -> dict:
    with open(get_rule('PATHS', 'STATS'), 'r', encoding='utf-8') as file:
        content = file.read()
        unpacked_data = json.loads(content)
    return unpacked_data


default_stats = {
    'TIPS_USED_TODAY': 0,
    'TIPS_USED': 0,
    'SHARDS_GIVEN': 0,
    'SHARDS_RECEIVED': 0,
    'TIPS_RECEIVED': 0,
    'TIPS_RECEIVED_TODAY': 0
}


def rgb_to_hex(rgb: tuple) -> str:
    """Converts RGB color to HEX."""
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'
