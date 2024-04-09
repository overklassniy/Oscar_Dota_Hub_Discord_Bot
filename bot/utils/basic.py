import datetime
import json


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


def get_now():
    now = datetime.datetime.now()
    return now.strftime("%H:%M:%S")


def is_allowed_string(s, allowed_string):
    allowed_chars = set(allowed_string)
    return set(s).issubset(allowed_chars)
