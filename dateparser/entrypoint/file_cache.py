import json

"""
Used to Cache data from the inner working of dateparser
"""

def clear_cache():
    with open('json_data_cache.json', 'w') as outfile:
        base_data = {"directives": [], "translation": ""}
        json.dump(base_data, outfile)

def save_cache(save_data):
    with open('json_data_cache.json', 'w') as outfile:
        json.dump(save_data, outfile)

def add_directive(new_data):
    save_data = get_directive()
    save_data["directives"].append(new_data)
    save_cache(save_data)

def add_translation(new_data):
    save_data = get_directive()
    save_data["translation"] = new_data
    save_cache(save_data)

def get_directive():
    with open('json_data_cache.json') as json_file:
        data = json.load(json_file)
        return data
