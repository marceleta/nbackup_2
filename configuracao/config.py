import json
import platform

from json_modelos.modelos import Backup, Usuario, Config_server
from util.util import Log

class Configuracao:

    def __init__(self):
        self._config_path()
        self._set_usuario()
        self._set_server()
        self._set_backup()



    def _set_usuario(self):

        with open(self._path + 'configuracao/login.json') as login_json:
            _json = json.load(login_json)
            self._usuarios = []
            for u in _json['login']:
                usuario = Usuario(u)
                self._usuarios.append(usuario)
        Log.info('[configuracao] leitura do arquivo login.json')

    def _set_server(self):
        with open(self._path + 'configuracao/server.json') as server_json:
            _json = json.load(server_json)
            self._server = Config_server(_json['server'])
        Log.info('[configuracao] leitura do arquivo server.json')


    def _set_backup(self):
        with open(self._path + 'configuracao/backup_list.json') as backup_json:
            data = json.load(backup_json)
            b = data['backups']
            self._backup_list = []
            for i in b:
                backup = Backup(i)
                self._backup_list.append(backup)
        Log.info('[configuracao] leitura do arquivo backup_list.json')

    def salvar_config_bkps(self, bkps):
        string = json.dumps(bkps)
        with open(self._path + 'backup_list.json', 'w') as backup_file:
            backup_file.write(string)
        Log.info('[configuracao] escrita das configuracoes recebidas do ncliente')

    @staticmethod
    def os_system():
        return platform.system()

    def _config_path(self):
        if self.os_system() == 'Windows':
            self._path = 'c:/nbackup/'
        else:
            self._path = '/home/marcelo/python/nbackup/'

    def get_path(self):
        return self._path

    def get_usuarios(self):
        return self._usuarios

    def get_server_config(self):
        return self._server

    def get_backups(self):
        return self._backup_list
