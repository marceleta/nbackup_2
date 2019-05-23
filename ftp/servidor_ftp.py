from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import MultiprocessFTPServer
from threading import Thread
from configuracao.config import Configuracao

class Gestao_ftp:

        def __init__(self):
            self._config = Configuracao()
            self._ftp = self._config.get_server_config().config_ftp()
            print('ftp: {}'.format(self._ftp.host))
            self._ftp_andamento = {}
            self._ftp_finalizado = []
            self._erros = {}


        def adicionar(self, info_ftp):
            self._info_ftp = info_ftp
            thread = Ftp_thread(self._ftp, info_ftp['path'], info_ftp['nome'])
            self._ftp_andamento[info_ftp['nome']] = thread
            thread.start()

            resposta = {
                'resposta':'ftp_pronto_download',
                'conteudo':self._info_ftp['nome']
            }
            print('servidor_ftp:adicionar {}'.format(resposta))
            return resposta


        def desligar(self, nome_backup):
            is_desligado = False
            try:
                thread = self._ftp_andamento[nome_backup]
                thread.desligar_servidor()
                self._ftp_finalizado.append(thread)
                del self._ftp_andamento[nome_backup]
                is_desligado = thread.is_desligado()
            except KeyError:
                self._erros['KeyError'] = 'ftp {} nao encontrado'.format(nome_backup)

            return is_desligado

        def get_em_andamento(self):
            return self._ftp_andamento

        def is_rodando_ftp(self):
            is_rodando = False
            keys = self._ftp_andamento.keys()
            print('is_rodando:keys {}'.format(keys))
            for key in keys:
                thread = self._ftp_andamento[key]
                is_rodando = thread.is_desligado()

            return is_rodando

        def is_erros(self):
            return (len(self._erros) > 0)

        def get_erros(self):
            return self._erros

        def get_ftp_finalizados(self):
            return self._ftp_andamento


class Ftp_thread(Thread):

    def __init__(self, config_ftp, diretorio, nome):
        Thread.__init__(self, name=nome)
        self._servidor_ftp = Servidor_ftp(config_ftp, diretorio)
        self._is_desligado = False



    def run(self):
        self._servidor_ftp.iniciar_servidor()

    def get_servidor_ftp(self):
        return self._servidor_ftp

    def desligar_servidor(self):
        self._servidor_ftp.desligar_servidor()
        self._is_desligado = True


    def is_desligado(self):
        return self._is_desligado


class Servidor_ftp:

    def __init__(self, config_ftp, diretorio):
        '''
        config_ftp = classe Config_ftp
        diretorio = diretorio a ser compartilhado
        '''
        self._config = config_ftp
        self._dir = diretorio
        self._config_server()


    def _config_server(self):
        print('usuario: {}'.format(self._config.usuario))
        print('senha: {}'.format(self._config.senha))
        print('dir: {}'.format(self._dir))
        print('host: {}'.format(self._config.host))
        print('porta: {}'.format(self._config.porta))
        authorizer = DummyAuthorizer()
        authorizer.add_user(self._config.usuario, self._config.senha, self._dir, perm=self._config.permissao)
        handler = FTPHandler
        handler.authorizer = authorizer
        self._server = MultiprocessFTPServer((self._config.host, self._config.porta), handler)


    def iniciar_servidor(self):
        self._server.serve_forever()


    def desligar_servidor(self):
        self._server.close_all()
