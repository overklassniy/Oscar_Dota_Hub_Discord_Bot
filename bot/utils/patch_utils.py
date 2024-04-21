import json

import discord
from utils.basic import *


def is_allowed_patch_string(s: str) -> bool:
    if is_allowed_string(s, allowed_string=get_rule('STRINGS', 'ALLOWED_PATCH_STRING')) and '.' in s and '7' == s[0] and '.' == s[1]:
        return True
    return False


def is_patch_new(patch_number: str, ctx: discord.ApplicationContext):
    ru_role_id = get_rule('ROLES_IDS', 'RU')
    en_role_id = get_rule('ROLES_IDS', 'EN')
    if ru_role_id in [y.id for y in ctx.author.roles]:
        lang = ru_role_id
    else:
        lang = en_role_id
    patches_info = get_patches_info()
    done = patches_info['READY']
    abandoned = patches_info['ABANDONED']
    if patch_number in abandoned:
        text1 = f'The {patch_number} is ABANDONED'
        if lang == ru_role_id:
            text1 = f'{patch_number} НЕ БУДЕТ СДЕЛАН'
        return False, text1
    if patch_number in done:
        text2 = f'The {patch_number} is READY'
        if lang == ru_role_id:
            text2 = f'{patch_number} уже СДЕЛАН'
        return False, text2
    text3 = f'The {patch_number} is NEW'
    if lang == ru_role_id:
        text3 = f'{patch_number} будет СДЕЛАН'
    return True, text3


def get_patches_info() -> dict:
    patches_info = json.load(open(get_rule('PATHS', 'PATCHES_INFO'), 'r'))
    return patches_info


def add_ready_patch(patch_number: str):
    patches_info = get_patches_info()
    ready_patches = patches_info['READY']
    ready_patches.append(patch_number)
    patches_info['READY'] = ready_patches
    json.dump(patches_info, open(get_rule('PATHS', 'PATCHES_INFO'), 'w'))
    return f'Wrote {patch_number} to READY'


def add_abandoned_patch(patch_number: str):
    patches_info = get_patches_info()
    ready_patches = patches_info['ABANDONED']
    ready_patches.append(patch_number)
    patches_info['ABANDONED'] = ready_patches
    json.dump(patches_info, open(get_rule('PATHS', 'PATCHES_INFO'), 'w'))
    return f'Wrote {patch_number} to ABANDONED'


def get_requested_patch(request_id):
    patches_info = get_patches_info()
    requested_patches = patches_info['REQUESTED']
    patch_number = requested_patches[request_id]
    return patch_number


def add_requested_patch(request_id, patch_number: str):
    patches_info = get_patches_info()
    requested_patches = patches_info['REQUESTED']
    requested_patches[request_id] = patch_number
    patches_info['REQUESTED'] = requested_patches
    json.dump(patches_info, open(get_rule('PATHS', 'PATCHES_INFO'), 'w'))
    return f'Wrote {patch_number} to REQUESTED (id = {request_id})'


def delete_requested_patch(request_id):
    patches_info = get_patches_info()
    requested_patches = patches_info['REQUESTED']
    patch_number = requested_patches[request_id]
    del requested_patches[request_id]
    patches_info['REQUESTED'] = requested_patches
    json.dump(patches_info, open(get_rule('PATHS', 'PATCHES_INFO'), 'w'))
    return f'Deleted {patch_number} from REQUESTED (id = {request_id})'


def create_script(depot_manifest_dict: dict, max_timestamp: float):
    if max_timestamp >= 1651700755:
        template = f'''download_depot 570 228989 {depot_manifest_dict[228989][0]} //vc2022       https://steamdb.info/depot/228983/manifests/
download_depot 570 228990 {depot_manifest_dict[228990][0]} //dx2010       https://steamdb.info/depot/228990/manifests/
download_depot 570 373302 {depot_manifest_dict[373302][0]} //win32        https://steamdb.info/depot/373302/manifests/
download_depot 570 373303 {depot_manifest_dict[373303][0]} //win64        https://steamdb.info/depot/373303/manifests/
download_depot 570 373301 {depot_manifest_dict[373301][0]} //content1     https://steamdb.info/depot/373301/manifests/
download_depot 570 381451 {depot_manifest_dict[381451][0]} //content2     https://steamdb.info/depot/381451/manifests/
download_depot 570 381452 {depot_manifest_dict[381452][0]} //content3     https://steamdb.info/depot/381452/manifests/
download_depot 570 381453 {depot_manifest_dict[381453][0]} //content4     https://steamdb.info/depot/381453/manifests/
download_depot 570 381454 {depot_manifest_dict[381454][0]} //content5     https://steamdb.info/depot/381454/manifests/
download_depot 570 381455 {depot_manifest_dict[381455][0]} //content6     https://steamdb.info/depot/381455/manifests/
download_depot 570 373307 {depot_manifest_dict[373307][0]} //lowviolence  https://steamdb.info/depot/373307/manifests/
download_depot 570 381456 {depot_manifest_dict[381456][0]} //russian      https://steamdb.info/depot/381456/manifests/
download_depot 570 373308 {depot_manifest_dict[373308][0]} //korean       https://steamdb.info/depot/373308/manifests/
download_depot 570 373309 {depot_manifest_dict[373309][0]} //chinese      https://steamdb.info/depot/373309/manifests/
download_depot 570 381450 {depot_manifest_dict[381450][0]} //workshop     https://steamdb.info/depot/381450/manifests/
download_depot 570 401531 {depot_manifest_dict[401531][0]} //opengl       https://steamdb.info/depot/401531/manifests/
download_depot 570 401535 {depot_manifest_dict[401535][0]} //vulkancommon https://steamdb.info/depot/401535/manifests/
download_depot 570 401536 {depot_manifest_dict[401536][0]} //vulkanwin64  https://steamdb.info/depot/401536/manifests/'''
    else:
        template = f'''download_depot 570 228983 {depot_manifest_dict[228983][0]} //vc2010       https://steamdb.info/depot/228983/manifests/
download_depot 570 228990 {depot_manifest_dict[228990][0]} //dx2010       https://steamdb.info/depot/228990/manifests/
download_depot 570 373302 {depot_manifest_dict[373302][0]} //win32        https://steamdb.info/depot/373302/manifests/
download_depot 570 373303 {depot_manifest_dict[373303][0]} //win64        https://steamdb.info/depot/373303/manifests/
download_depot 570 373301 {depot_manifest_dict[373301][0]} //content1     https://steamdb.info/depot/373301/manifests/
download_depot 570 381451 {depot_manifest_dict[381451][0]} //content2     https://steamdb.info/depot/381451/manifests/
download_depot 570 381452 {depot_manifest_dict[381452][0]} //content3     https://steamdb.info/depot/381452/manifests/
download_depot 570 381453 {depot_manifest_dict[381453][0]} //content4     https://steamdb.info/depot/381453/manifests/
download_depot 570 381454 {depot_manifest_dict[381454][0]} //content5     https://steamdb.info/depot/381454/manifests/
download_depot 570 381455 {depot_manifest_dict[381455][0]} //content6     https://steamdb.info/depot/381455/manifests/
download_depot 570 373307 {depot_manifest_dict[373307][0]} //lowviolence  https://steamdb.info/depot/373307/manifests/
download_depot 570 381456 {depot_manifest_dict[381456][0]} //russian      https://steamdb.info/depot/381456/manifests/
download_depot 570 373308 {depot_manifest_dict[373308][0]} //korean       https://steamdb.info/depot/373308/manifests/
download_depot 570 373309 {depot_manifest_dict[373309][0]} //chinese      https://steamdb.info/depot/373309/manifests/
download_depot 570 381450 {depot_manifest_dict[381450][0]} //workshop     https://steamdb.info/depot/381450/manifests/
download_depot 570 401531 {depot_manifest_dict[401531][0]} //opengl       https://steamdb.info/depot/401531/manifests/
download_depot 570 401535 {depot_manifest_dict[401535][0]} //vulkancommon https://steamdb.info/depot/401535/manifests/
download_depot 570 401536 {depot_manifest_dict[401536][0]} //vulkanwin64  https://steamdb.info/depot/401536/manifests/'''
    return template
