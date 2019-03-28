import json

class Conversor:

    def __init__(self):
        pass
    @staticmethod
    def dict_to_json(value):
        return json.dumps(value)
    
    @staticmethod
    def json_to_dict(value):
        return json.loads(value)
