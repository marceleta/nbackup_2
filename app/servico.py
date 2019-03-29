import datetime
import backup
import arquivo
import sys
from abc import ABC, abstractmethod

class Template_servico(object):

    bkp_diario = 'diario'
    bkp_semanal = 'semanal'
    bkp_mensal = 'mensal'

    def __init__(self, backup):
        self._backup = backup

    @abstractmethod
    def verifica_execucao(self):
        '''
        Returna (True/False) se os requisitos em backup foram satisfeitos
        '''
        pass

    @abstractmethod
    def is_hora_exec(self):

    @abstractmethod
    def executar(self):
        pass

    @abstractmethod
    def executa_sc_pre(self):
        pass

    @abstractmethod
    def executa_sc_pos(self):
        pass

    @abstractmethod
    def verifica_arquivo(self):
        pass

    @abstractmethod
    def gerar_resposta():
        pass

    @abstractmethod
    def get_arquivo_defincao():
        pass



class Servico(Template_servico):
    dia_semana = [
        segunda,
        terca,
        quarta,
        quinta,
        sexta,
        sabado,
        domingo
    ]

    def __init__(self, backup):
        super.__init__(backup)
        self._backup = backup


    def verifica_execucao(self):

        if

    def executar(self):



    def _is_hora_exec(self, hora):
        is_hora_exec = False

        agora = datetime.datetime.now()
        agora_minute = int(agora.hour)*60 + int(agora.minute)

        bhora = self._conv_hora(hora)
        bhora_minute = int(bhora.hour)*60 + int(bhora.minute)

        print("agora_minute: {}".format(agora_minute))
        print("bhora_minute: {}".format(bhora_minute))

        if bhora_minute > agora_minute:
            is_hora_exec = True

        return is_hora_exec


    def _conv_hora(self, hora):
        return datetime.datetime.strftime(data, '%H:%M')
