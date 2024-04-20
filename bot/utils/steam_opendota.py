import os

import opendota
from dotenv import load_dotenv
from steam_web_api import Steam
from utils.basic import *

load_dotenv()

client_opendota = opendota.OpenDota()

steamwebapi_key = os.getenv('STEAMWEBAPI-KEY')
client_steam = Steam(steamwebapi_key)


def steamid64_to_steamid32(commid):
    steamid64ident = 76561197960265728
    steamidacct = int(commid) - steamid64ident
    return steamidacct


def steamurl_to_steamid64(url):
    if url[:35] != 'https://steamcommunity.com/profiles':
        if url[-1] == '/':
            profile_id = url.split('/')[-2]
        else:
            profile_id = url.split('/')[-1]
        response = client_steam.users.search_user(profile_id)
        steamid64 = int(response['player']['steamid'])
        return steamid64
    junk_steamid64 = url[35:]
    steamid64 = int(junk_steamid64.replace('/', ''))
    return steamid64


def get_nickname(url):
    id = steamurl_to_steamid64(url)
    response = client_steam.users.get_user_details(str(id))
    return response['player']['personaname']


def get_realname(url):
    idd = steamurl_to_steamid64(url)
    response = client_steam.users.get_user_details(str(idd))
    try:
        return response['player']['realname']
    except Exception:
        return 'no_name'


def get_avatar(url):
    id = steamurl_to_steamid64(url)
    response = client_steam.users.get_user_details(str(id))
    return response['player']['avatarfull']


def steamurl_to_steamid32(url):
    steamid64 = steamurl_to_steamid64(url)
    steamid32 = steamid64_to_steamid32(steamid64)
    return steamid32


def get_rating_score(steamid32):
    tier_to_score = {11: 10, 12: 150, 13: 300, 14: 460, 15: 610, 21: 770, 22: 920, 23: 1080, 24: 1230, 25: 1400, 31: 1540, 32: 1700, 33: 1850,
                     34: 2000, 35: 2150, 41: 2310, 42: 2450, 43: 2610, 44: 2770, 45: 2930, 51: 3080, 52: 3230, 53: 3390, 54: 3540, 55: 3700, 61: 3850,
                     62: 4000, 63: 4150, 64: 4300, 65: 4460, 71: 4620, 72: 4820, 73: 5020, 74: 5220, 75: 5420}
    response = client_opendota.get_player(steamid32)
    if response:
        try:
            rank_tier = int(response['rank_tier'])
        except Exception:
            rank_tier = 11
    else:
        rank_tier = 11
    if rank_tier > 75:
        solo_competitive_rank = 5420 + 100 * (rank_tier - 75)
    else:
        solo_competitive_rank = tier_to_score[rank_tier]
    return solo_competitive_rank


def get_mmr_from_discord(dsid: str):
    users = get_users()
    try:
        steam64 = users[dsid]
    except Exception as e:
        return 10
    score = get_rating_score(steamid64_to_steamid32(steam64))
    print(f'[{get_now()}] Getting MMR from {dsid}: {steam64} - {score}')
    return score
