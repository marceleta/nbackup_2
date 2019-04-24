import json
import usuario
import server
import backup
import platform


class Configuracao:

    def __init__(self):
        self._set_usuario()
        self._set_server()
        self._set_backup()


    def _set_usuario(self):

        with open('login.json') as login_json:
            self._usuarios = json.load(login_json)
            #self.list_usuarios = []
            #for p in data['login']:
            #    self.usuario = usuario.Usuario(p['usuario'], p['senha'])
            #    self.list_usuarios.append(self.usuario)

    def _set_server(self):

        with open('server.json') as server_json:
            self._server = json.load(server_json)
            #p = data['server']
            #for i in p:
            #    self.server_config = server.Server(i['host'], int(i['porta']),
            #                                        int(i['qtd_conecoes']))

    def _set_backup(self):

        with open('backup_list.json') as backup_json:
            data = json.load(backup_json)
            b = data['backup']
            self._backup_list = []
            for i in b:
            #    self.backup = backup.Backup(i['nome'], i['path'], i['periodo'], i['dia_semana'],
            #                    i['hora_execucao'], i['sc_pre_execucao'], i['sc_pos_execucao'])
                self._backup = backup.Backup(i)
                self._backup_list.append(self._backup)
                
    @staticmethod
    def os_system():
        return platform.system()

    def get_usuarios(self):
        return self._usuarios

    def get_server_config(self):
        return self._server

    def get_backups(self):
        return self._backup_list
