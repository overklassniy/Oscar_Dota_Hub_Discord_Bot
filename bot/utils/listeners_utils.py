import json


def get_deleted_reactions():
    deleted_reactions = json.load(open('data/deleted_reactions.json', 'r'))
    # TODO: сделать вывод в формате списка, собрав все удаленные реакции из всех каналов в один (не забыв указать канал из которого забирался) и отсортировав по возрастанию где null (None) идут самыми ранними
    return deleted_reactions


def write_deleted_reactions(channel_name: str, data: dict):
    deleted_reactions = json.load(open('data/deleted_reactions.json', 'r'))
    if channel_name not in deleted_reactions.keys():
        deleted_reactions[channel_name] = []
    deleted_reactions[channel_name].append(data)
    json.dump(deleted_reactions, open('data/deleted_reactions.json', 'w'))
    return f'Wrote a new deleted reaction to {channel_name}'
