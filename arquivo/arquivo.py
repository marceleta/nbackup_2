
class Arquivo:

    def __init__(self, nome, path, hash_verificacao, data_criacao, tamanho):
        self._nome = nome
        self._path = path
        self._hash_verificacao = hash_verificacao
        self._data_criacao = data_criacao
        self._tamanho = tamanho

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, value):
        self._nome = nome

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def hash_verificacao(self):
        return self._hash_verificacao

    @hash_verificacao.setter
    def hash_verificacao(self, value):
        self._hash_verificacao = value

    @property
    def data_criacao(self):
        return self._data_criacao

    @data_criacao.setter
    def data_criacao(self, value):
        self._data_criacao = value

    @property
    def tamanho(self):
        return self._tamanho

    @tamanho.setter
    def tamanho(self, tamanho):
        self._tamanho = tamanho
