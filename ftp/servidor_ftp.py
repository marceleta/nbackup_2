from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from threading import Thread
from configuracao.config import Configuracao
from util.util import Log

class Gestao_ftp:

        def __init__(self):
            self._config = Configuracao()
            self._ftp = self._config.get_server_config().config_ftp()
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
            Log.info('adicionando e iniciando thread ftp: {}'.format(info_ftp['nome']))

            return resposta


        def desligar(self, nome_backup):
            is_desligado = False
            try:
                thread = self._ftp_andamento[nome_backup]
                thread.desligar_servidor()
                self._ftp_finalizado.append(thread)
                del self._ftp_andamento[nome_backup]
                is_desligado = thread.is_desligado()
                Log.info('desligando ftp: {}'.format(nome_backup))
            except KeyError:
                Log.error('KeyError: ftp: {} nao encontrado'.format(nome_backup))
                self._erros['KeyError'] = 'ftp {} nao encontrado'.format(nome_backup)

            return is_desligado

        def get_em_andamento(self):
            return self._ftp_andamento

        def is_rodando_ftp(self):
            is_rodando = False
            keys = self._ftp_andamento.keys()
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
        self._nome = nome
        self._servidor_ftp = Servidor_ftp(config_ftp, diretorio)
        self._is_desligado = False



    def run(self):
        self._servidor_ftp.iniciar_servidor()
        Log.info('iniciando thread ftp: {}'.format(self._nome))

    def get_servidor_ftp(self):
        return self._servidor_ftp

    def desligar_servidor(self):
        self._servidor_ftp.desligar_servidor()
        self._is_desligado = True
        Log.info('desligando thread ftp: {}'.format(self._nome))


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
        authorizer = DummyAuthorizer()
        authorizer.add_user(self._config.usuario, self._config.senha, self._dir, perm=self._config.permissao)
        handler = FTPHandler
        handler.authorizer = authorizer
        #self._server = MultiprocessFTPServer((self._config.host, self._config.porta), handler)
        self._server = FTPServer((self._config.host, self._config.porta), handler)


    def iniciar_servidor(self):
        self._server.serve_forever(timeout=10)


    def desligar_servidor(self):
        self._server.close_all()
