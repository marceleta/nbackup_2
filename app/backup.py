import datetime

class Backup:
    def __init__(self,nome, path, periodo, dia_semana, hora_execucao,
                    sc_pre_execucao, sc_pos_execucao):

        self._nome = nome
        self._path = path
        self._periodo = periodo
        self._dia_semana = dia_semana
        self._hora_execucao = hora_execucao
        self._sc_pre_execucao = sc_pre_execucao
        self._sc_pos_execucao = sc_pos_execucao

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, value):
        self._nome = value

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def periodo(self):
        return self._periodo

    @periodo.setter
    def periodo(self, value):
        self._periodo = value

    @property
    def dia_semana(self):
        return self._format_hora(self._dia_semana)

    @dia_semana.setter
    def dia_semana(self, value):
        self._dia_semana = value

    def _format_hora(self, hora):
        h = datetime.datetime.strptime(hora,'%H:%M')

        return h

    @property
    def hora_execucao(self):
        return self._hora_execucao

    @hora_execucao.setter
    def hora_execucao(self, value):
        self._hora_execucao = value

    @property
    def sc_pre_execucao(self):
        return self._sc_pre_execucao

    @sc_pre_execucao.setter
    def sc_pre_execucao(self, value):
        self._sc_pre_execucao = value

    @property
    def sc_pos_execucao(self):
        return self._sc_pos_execucao

    @sc_pos_execucao.setter
    def sc_pos_execucao(self, value):
        self._sc_pos_execucao = value
