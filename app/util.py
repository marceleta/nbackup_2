import json
import hashlib

class Conversor:

    def __init__(self):
        pass
    @staticmethod
    def dict_to_json(value):
        return json.dumps(value)

    @staticmethod
    def json_to_dict(value):
        return json.loads(value)


class Gerar_md5:

    @staticmethod
    def get_md5(arquivo):
        md5 = hashlib.md5()
        with open(arquivo, 'rb') as file:
            for chuck in iter(lambda: file.read(4096). b""):
                md5.update(chuck)

        return md5.hexdigest()
