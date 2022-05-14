
from dateparser import parse
from entrypoint.file_cache import clear_cache, get_directive

"""
An entrypoint for dateparser that exposes structure in terms of python datetime [Format Code List](https://www.programiz.com/python-programming/datetime/strftime)
"""

def get_structure(string, settings=None):
    clear_cache()

    dt_object = parse(string, settings)

    if not dt_object:
        return {"datetime_object": None, "structure": None}

    cache_data = get_directive()
    structure = cache_data["translation"]

    for patters in cache_data["directives"]:
        string = patters.get("string")
        directive = patters.get("directive")
        structure = structure.replace(string, directive, 1)

    return {"datetime_object": dt_object, "structure": structure}
