

class Usuario(object):

    def __init__(self, login, senha):
            self._login = login
            self._senha = senha

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, value):
        self._login = value

    @property
    def senha(self):
        return self._senha

    @senha.setter
    def senha(self, value):
        self._senha = value
