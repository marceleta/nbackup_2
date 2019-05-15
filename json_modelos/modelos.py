
class Config_server:

    def __init__(self, dict):
        self._host = dict['host']
        self._porta = dict['porta']
        self._qtd_conecoes = dict['qtd_conecoes']
        self._ftp = Config_ftp(dict['ftp'])

    @property
    def host(self):
        return self._host

    @property
    def porta(self):
        return self._porta

    @property
    def qtd_conecoes(self):
        return self._qtd_conecoes

    @property
    def config_ftp(self):
        return self._ftp



class Config_ftp:

    def __init__(self, dict):
        '''
        Recebe um dicionario com as info de configuracao
        '''
        self._usuario = dict['usuario']
        self._senha = dict['senha']
        self._permissao = dict['permissao']
        self._host = dict['host']
        self._porta = int(dict['porta'])


    @property
    def usuario(self):
        return self._usuario

    @property
    def senha(self):
        return self._senha

    @property
    def permissao(self):
        return self._permissao

    @property
    def host(self):
        return self._host

    @property
    def porta(self):
        return self._porta

class Usuario:

    def __init__(self, dict):
        self._usuario = dict['usuario']
        self._senha = dict['senha']

    @property
    def usuario(self):
        return self._usuario

    @property
    def senha(self):
        return self._senha
