import datetime
import backup
import arquivo
import sys
from config import Configuracao
from abc import ABC, abstractmethod
import subprocess

class Template_servico(object):
    dia_semana = [
        segunda,
        terca,
        quarta,
        quinta,
        sexta,
        sabado,
        domingo
    ]

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
        pass

    def hora_para_minutos(self, hora):
        temp = datetime.time(hour=hora.hour, minute=hora.minute)
        minutos = (temp.hora)*60 + (temp.minute)

        return minutos

    @abstractmethod
    def executar(self, backup):
        pass

    @abstractmethod
    def executa_sc_pre(self, backup):
        pass

    @abstractmethod
    def executa_sc_pos(self):
        pass

    @abstractmethod
    def executa_backup(self, backup):
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



class Servico_diario(Template_servico):


    def __init__(self, backup):
        super.__init__(backup)
        self._backup = backup

    def verifica_execucao(self):
        is_executar = False
        lista_horario = self._backup['backup']['hora_execucao']

        for str_hora in lista_horario:
            _hora = self._conv_hora(str_hora)

            if self._is_hora_exec(_hora):
                is_executar = True

        return is_executar

    def executar(self, backup):
        pass

    def executa_sc_pre(self, backup):
        execucao = 'OK'
        str_sc = backup['sc_pre_execucao']
        if str_sc == '':
            process = subprocess.Popen(str_sc, shell=True, stdout=subprocess.PIPE)
            output, erro = process.communicate()
            if erro == None:
                execucao = 'ERRO'

        return execucao

    def executa_sc_pos(self, backup):
        execucao = 'OK'
        str_sc =backup['sc_pos_execucao']
        if str_sc == '':
            process = subprocess.Popen(str_sc, shell=True, stdout=subprocess.PIPE)
            output, erro = process.communicate()
            if erro == None:
                execucao = 'ERRO'

        return execucao

    def executa_backup(self, backup):
        execucao = 'OK'
        str_sc = backup['sc_backup']
        if str_sc == '':
            processo = subprocess.Popen(str_sc, shell=True, stdout=subprocess.PIPE)
            output, erro = processo.communicate()
            if erro == None:
                execucao = 'ERRO'

        return execucao

    def _is_hora_exec(self, hora):
        t = datetime.datetime.now()
        minutes_now = super.hora_para_minutos(t)

        minutes_bkp = super.hora_para_minutos(hora)

        return (minutes_now >= minutes_bkp)


    def _conv_hora(self, hora):
        return datetime.datetime.strftime(hora, '%H:%M')
