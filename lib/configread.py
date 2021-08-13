import json
import copy

__config = {};
__white_list = []

with open('config.json', 'r') as config_file:
    __config=json.loads(config_file.read())

if 'white_list' in __config:
    __white_list = __config['white_list']

def config ():
    return copy.deepcopy(__config)

def whiteList():
    return copy.deepcopy(__white_list)

