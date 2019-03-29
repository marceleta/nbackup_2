
class Arquivo:

    def __init__(self, nome=None, hash_verificacao=None, data_criacao=None):
        self._nome = nome
        self._hash_verificacao = hash_verificacao
        self._data_criacao = data_criacao

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, value):
        self._nome = nome
    @property
    def hash_verificacao(self):
        return self._hash_verificacao

    @hash_verificacao.setter
    def hash_verificacao(self, value)
        self._hash_verificacao = value

    @property
    def data_criacao(self):
        return self._data_criacao

    @data_criacao.setter
    def data_criacao(self, value):
        self._data_criacao = value
