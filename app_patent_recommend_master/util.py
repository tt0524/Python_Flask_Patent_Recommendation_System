import json as JSON
from flask import json

request_json = None

ERROR_LOG = __name__ + ' juanchen: '


def request_form_to_json(request):
    try:
        return JSON.loads(json.dumps(request.form))
    except Exception:
        print(ERROR_LOG + 'request form to json failed')
        return None


def string_to_json(json_str):
    try:
        return JSON.loads(json_str)
    except Exception:
        print(ERROR_LOG + 'string to json failed')
        return None


def json_to_string(json_obj):
    try:
        return JSON.dumps(json_obj)
    except Exception:
        print(ERROR_LOG + 'json to string failed')
        return None


def stringlist_to_json_list(data):
    try:
        options = []
        for choice in data.split(';'):
            options.append({'content': choice})
        return options
    except Exception:
        print(ERROR_LOG + 'string list to json list failed')
        return None
