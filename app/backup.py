import datetime

class Backup:
    #def __init__(self,nome, path, periodo, dia_semana, hora_execucao,
    #                sc_pre_execucao, sc_pos_execucao):
    #
    #    self._nome = nome
    #    self._path = path
    #    self._periodo = periodo
    #    self._dia_semana = dia_semana
    #    self._hora_execucao = hora_execucao
    #    self._sc_pre_execucao = sc_pre_execucao
    #    self._sc_pos_execucao = sc_pos_execucao

    def __init__(self, dict):
        self._dict = dict

    @property
    def nome(self):
        #return self._nome
        return self._dict['nome']

    @nome.setter
    def nome(self, value):
        #self._nome = value
        self._dict['nome'] = value

    @property
    def path(self):
        #return self._path
        return self._dict['path']

    @path.setter
    def path(self, value):
        #self._path = value
        self._dict['path'] = value

    @property
    def periodo(self):
        #return self._periodo
        return self._dict['periodo']

    @periodo.setter
    def periodo(self, value):
        #self._periodo = value
        self._dict['periodo'] = periodo

    @property
    def dia_semana(self):
        #return self._format_hora(self._dia_semana)
        return self._format_hora(self._dict['dia_semana'])

    @dia_semana.setter
    def dia_semana(self, value):
        #self._dia_semana = value
        self._dict['dia_semana'] = value

    def _format_hora(self, hora):
        h = datetime.datetime.strptime(hora,'%H:%M')

        return h

    @property
    def hora_execucao(self):
        #return self._hora_execucao
        return self._dict['hora_execucao']

    @hora_execucao.setter
    def hora_execucao(self, value):
        #self._hora_execucao = value
        self._dict['hora_execucao'] = value

    @property
    def sc_pre_execucao(self):
        #return self._sc_pre_execucao
        return self._dict['sc_pre_execucao']

    @sc_pre_execucao.setter
    def sc_pre_execucao(self, value):
        #self._sc_pre_execucao = value
        self._dict['sc_pre_execucao'] = value

    @property
    def sc_pos_execucao(self):
        #return self._sc_pos_execucao
        return self._dict['sc_pos_execucao']

    @sc_pos_execucao.setter
    def sc_pos_execucao(self, value):
        #self._sc_pos_execucao = value
        self._dict['sc_pos_execucao'] = value

    def get_dict(self):
        return self._dict


class Backup_dict:

    @staticmethod
    def get_dict(self, lista_backups):
        '''
        Converte uma lista de backups em um dicionario
        '''
        dict = {"Backup":lista_backups}
        return dict
