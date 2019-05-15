import json
import usuario
import server
import backup
import platform
from json_modelos.modelos import Config_server, Usuario

class Configuracao:

    def __init__(self):
        self._config_path()
        self._set_usuario()
        self._set_server()
        self._set_backup()
        self._set_config_ftp()



    def _set_usuario(self):

        with open(self._path + 'login.json') as login_json:
            _json = json.load(login_json)
            self._usuarios = []
            for u in _json['usuario']:
                usuario = Usuario(u)
                self._usuarios.append(usuario)

    def _set_server(self):
        with open(self._path + 'server.json') as server_json:
            _json = json.load(server_json)
            self._server = Config_server(_json['server'])


    def _set_backup(self):
        with open(self._path + 'backup_list.json') as backup_json:
            data = json.load(backup_json)
            b = data['backups']
            self._backup_list = []
            for i in b:
                self._backup = backup.Backup(i)
                self._backup_list.append(self._backup)

    def salvar_config_bkps(self, bkps):
        string = json.dumps(bkps)
        with open(self._path + 'backup_list.json', 'w') as backup_file:
            backup_file.write(string)

    @staticmethod
    def os_system():
        return platform.system()

    def _config_path(self):
        if self.os_system() == 'Windows':
            self._path = 'c:/nbackup/app/'
        else:
            self._path = '/home/marcelo/python/nbackup_2/app/'

    def get_usuarios(self):
        return self._usuarios

    def get_server_config(self):
        return self._server

    def get_backups(self):
        return self._backup_list
