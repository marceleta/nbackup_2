import json
import hashlib
import datetime
import logging

logging.basicConfig(level=logging.INFO, filename='nbackup.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M')


class Log:

    @staticmethod
    def debug(mensagem):
        logging.debug(mensagem)

    @staticmethod
    def info(mensagem):
        logging.info(mensagem)

    @staticmethod
    def warning(mensagem):
        logging.warning(mensagem)

    @staticmethod
    def error(mensagem):
        logging.error(mensagem)

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
            for chuck in iter(lambda: file.read(4096), b""):
                md5.update(chuck)

        return md5.hexdigest()

class Conv_data:

    @staticmethod
    def get_date_now():
        date_now = datetime.datetime.now()
        date = datetime.date(year=date_now.year, month=date_now.month, day=date_now.day)

        return date

    @staticmethod
    def str_to_time(str_hora):
        '''
        Recebe uma str no formato HH:MM e converte em datetime.time
        '''
        hora = None
        try:
            split_hora = str_hora.split(':')
            int_hora = int(split_hora[0])
            int_minutos = int(split_hora[1])
            hora = datetime.time(hour=int_hora, minute=int_minutos)
        except ValueError:
            hora = None

        return hora
