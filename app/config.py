import json
import usuario
import server
import backup


class Configuracao:

    def __init__(self):
        self._set_usuario()
        self._set_server()
        self._set_backup_list()


    def _set_usuario(self):

        with open('login.json') as login_json:
            data = json.load(login_json)
            self.list_usuarios = []
            for p in data['login']:
                self.usuario = usuario.Usuario(p['usuario'], p['senha'])
                self.list_usuarios.append(self.usuario)

    def _set_server(self):

        with open('server.json') as server_json:
            data = json.load(server_json)
            p = data['server']
            for i in p:
                self.server_config = server.Server(i['host'], int(i['porta']),
                                                    int(i['qtd_conecoes']))

    def _set_backup_list(self):

        with open('backup_list.json') as backup_json:
            data = json.load(backup_json)
            b = data['backup']
            self.backup_list = []
            for i in b:
                self.backup = backup.Backup(i['nome'], i['path'], i['periodo'], i['dia_semana'],
                                i['hora_execucao'], i['sc_pre_execucao'], i['sc_pos_execucao'])

                self.backup_list.append(self.backup)

    def get_usuarios(self):
        return self.list_usuarios

    def get_server_config(self):
        return self.server_config

    def get_backup(self):
        return self.backup_list
