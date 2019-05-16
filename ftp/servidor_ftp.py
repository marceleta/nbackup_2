from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import MultiprocessFTPServer
from threading import Thread
from configuracao.config import Configuracao

class Gestao_ftp:

    def __init__(self, diretorio, nome):
        self._dir = diretorio
        self._config = Configuracao()
        self._ftp_serv = Servidor_ftp(self._config.get_config_ftp(), self._dir)
        self._thread_ftp = Ftp_thread(self._ftp_serv, nome)


    def iniciar(self):
        self._thread_ftp.start()

    def desligar(self):
        self._thread_ftp.desligar_servidor()

    def get_nome(self):
        return self._thread_ftp.name

    def is_ativo(self):
        return self._thread_ftp.is_alive()

class Gestao_ftp:

    def __init__(self):
        self._loop_gestao = True
        self._thread_gestao = []
        self._ftp_em_espera = []
        self._ftp_em_andamento = []
        self._ftp_finalizados = []


    def adicionar(self, config_ftp, diretorio):
        c_ftp = Servidor_ftp(config_ftp, diretorio)
        thread = Ftp_thread(c_ftp, )






class Ftp_thread(Thread):

    def __init__(self, servidor_ftp, nome):
        Thread.__init__(self, name=nome)
        self._servidor = servidor_ftp

    def run(self):
        self._servidor.iniciar_servidor()

    def get_servidor_ftp(self):
        return self._servidor

    def desligar_servidor(self):
        self._servidor.desligar_servidor()


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
        self._server = MultiprocessFTPServer((self._config.host, self._config.porta), handler)

    def iniciar_servidor(self):
        self._server.serve_forever()


    def desligar_servidor(self):
        self._server.close_all()
