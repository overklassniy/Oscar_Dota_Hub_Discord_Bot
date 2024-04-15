import datetime
import json
from urllib.parse import urlparse


def get_config():
    rules = json.load(open('bot/config.json', 'r'))
    return rules


def get_rule(section, key):
    return get_config()[section][key]


def write_rule(section, key, value):
    rules = get_config()
    rules[section][key] = value
    json.dump(rules, open('/bot/config.json', 'w'))
    return rules


def get_now(need_date=True, need_date_only=False):
    now = datetime.datetime.now()
    if need_date:
        return now.strftime("%d/%m/%Y %H:%M:%S")
    if need_date_only:
        return now.strftime("%d/%m/%Y")
    return now.strftime("%H:%M:%S")


def is_allowed_string(s, allowed_string):
    allowed_chars = set(allowed_string)
    return set(s).issubset(allowed_chars)


def uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except AttributeError:
        return False
