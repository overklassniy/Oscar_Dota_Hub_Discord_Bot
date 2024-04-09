import json

from utils.basic import *


def is_allowed_patch_string(s):
    if is_allowed_string(s, allowed_string=get_rule('STRINGS', 'ALLOWED_PATCH_STRING')) and '.' in s and '7' == s[0] and '.' == s[1]:
        return True
    return False


def is_patch_new(patch_number: str):
    patches_info = get_patches_info()
    done = patches_info['READY']
    abandoned = patches_info['ABANDONED']
    if patch_number in abandoned:
        return False, f'The {patch_number} is ABANDONED'
    if patch_number in done:
        return False, f'The {patch_number} is READY'
    return True, f'The {patch_number} is NEW'


def get_patches_info():
    patches_info = json.load(open('data/patches_info.json', 'r'))
    return patches_info


def add_ready_patch(patch_number: str):
    patches_info = get_patches_info()
    ready_patches = patches_info['READY']
    ready_patches.append(patch_number)
    patches_info['READY'] = ready_patches
    json.dump(patches_info, open('data/patches_info.json', 'w'))
    return f'Wrote {patch_number} to READY'


def add_abandoned_patch(patch_number: str):
    patches_info = get_patches_info()
    ready_patches = patches_info['ABANDONED']
    ready_patches.append(patch_number)
    patches_info['ABANDONED'] = ready_patches
    json.dump(patches_info, open('data/patches_info.json', 'w'))
    return f'Wrote {patch_number} to ABANDONED'


def get_requested_patch(request_id):
    patches_info = get_patches_info()
    requested_patches = patches_info['REQUESTED']
    patch_number = requested_patches[request_id]
    return patch_number


def add_requested_patch(request_id, patch_number):
    patches_info = get_patches_info()
    requested_patches = patches_info['REQUESTED']
    requested_patches[request_id] = patch_number
    patches_info['REQUESTED'] = requested_patches
    json.dump(patches_info, open('data/patches_info.json', 'w'))
    return f'Wrote {patch_number} to REQUESTED (id = {request_id})'


def delete_requested_patch(request_id):
    patches_info = get_patches_info()
    requested_patches = patches_info['REQUESTED']
    patch_number = requested_patches[request_id]
    del requested_patches[request_id]
    patches_info['REQUESTED'] = requested_patches
    json.dump(patches_info, open('data/patches_info.json', 'w'))
    return f'Deleted {patch_number} from REQUESTED (id = {request_id})'
