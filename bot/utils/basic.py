import datetime
import json
from urllib.parse import urlparse


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


def uri_validator(url: str):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except AttributeError:
        return False


def write_users(data: dict):
    with open(get_rule('PATHS', 'USERS'), 'w', encoding='utf-8') as file:
        json.dump(data, file)


def get_users() -> dict:
    with open(get_rule('PATHS', 'USERS'), 'r', encoding='utf-8') as file:
        content = file.read()
        unpacked_data = json.loads(content)
    return unpacked_data
