import datetime
import sys
from abc import ABC, abstractmethod
import subprocess
import os, stat, time
import threading
from threading import Thread
import logging

from json_modelos.modelos import Backup
from backup.backup_zip import Backup_zip
from arquivo.arquivo import Arquivo
from util.util import Conv_data, Gerar_md5, Log
from configuracao.config import Configuracao

class Template_servico(object):


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
    def executa_sc_nativo(self):
        pass

    @abstractmethod
    def executa_sc_pre(self, backup):
        pass

    @abstractmethod
    def executa_sc_pos(self):
        pass

    @abstractmethod
    def executa_sc_backup(self, backup):
        pass

    @abstractmethod
    def verifica_arquivo(self):
        pass

    @abstractmethod
    def gerar_resposta():
        pass

    @abstractmethod
    def get_info_arquivo_backup():
        pass

class ServicoThread(Thread):
    def __init__(self, servico):
        #Thread.__init__(self, target=servico.executar(), name=servico.get_nome())
        Thread.__init__(self, name=servico.get_nome())
        self._servico = servico
        self._inicio = None
        self._final = None
        self._resultado = None

    def run(self):
        self._servico.executar()

    def get_nome(self):
        return self._servico.get_nome()

    def get_servico(self):
        return self._servico

    def set_inicio_thread(self, inicio):
        self._inicio = inicio

    def get_inicio_thread(self):
        return self._inicio

    def set_final_thread(self, final):
        self._final = final

    def get_final_thread(self):
        return self._final

class Servico_diario:

    def __init__(self, backup):
        self._backup = backup
        self._config = Configuracao()
        self._dict_resultado_executar = {}

    def get_nome(self):
        return self._backup.nome

    def get_backup(self):
        return self._backup

    def get_resultado(self):
        return self._dict_resultado_executar

    def verifica_execucao(self):
        is_executar = False
        hora_executar = self._backup.hora_execucao

        #converte str hora para datetime hora
        _hora_executar = self._conv_hora(hora_executar)
        #verifica se e a hora e maior ou menor
        if self._is_hora_exec(_hora_executar):
            is_executar = True

        return is_executar

    def executar(self):

        resultado = self.executa_sc_pre()
        self._dict_resultado_executar['executa_sc_pre'] = resultado

        if self._backup.backup_auto == 'Sim':
            resultado = self.executa_sc_backup()
            self._dict_resultado_executar['executa_backup_auto'] = resultado
        else:
            resultado = self.executa_sc_nativo()
            self._dict_resultado_executar['executa_sc_nativo'] = resultado

        resultado = self.executa_sc_pos()
        self._dict_resultado_executar['executa_sc_pos'] = resultado


    def executa_sc_pre(self):
        execucao = 'sucesso'
        str_sc = self._backup.sc_pre_execucao
        if str_sc == '':
            process = subprocess.Popen(str_sc, shell=True, stdout=subprocess.PIPE)
            output, erro = process.communicate()
            if erro == None:
                execucao = 'erro'

        return execucao

    def executa_sc_pos(self):
        execucao = 'sucesso'
        str_sc = self._backup.sc_pos_execucao
        print('executa_sc_pos: {}'.format(str_sc))
        if str_sc == '':
            process = subprocess.Popen(str_sc, shell=True, stdout=subprocess.PIPE)
            output, erro = process.communicate()
            if erro == None:
                execucao = 'erro'

        return execucao

    def executa_sc_backup(self):
        execucao = 'sucesso'
        str_sc = self._backup.sc_backup
        if str_sc == '':
            processo = subprocess.Popen(str_sc, shell=True, stdout=subprocess.PIPE)
            output, erro = processo.communicate()
            if erro == None:
                execucao = 'erro'

        return execucao

    def executa_sc_nativo(self):

        print('executa_sc_nativo: inicio da execucao')
        tmp_inicio = time.time()

        if self._backup.tipo == 'arquivo':
            path_origem = self._get_path_abs_origem()
        else:
            path_origem = self._backup.path_origem

        self.backup_zip = Backup_zip(self._backup.tipo, path_origem,
                                            self._get_path_abs_backup(), self._config.os_system())

        resultado = self.backup_zip.zip_backup()

        print('executa_sc_nativo: fim da execucao')
        tmp_final = time.time()
        print('tempo total: {}'.format(str(tmp_final - tmp_inicio)))
        

        return resultado   


    def verifica_backup_existe(self):
        '''
        verifica se o backup foi criado e a data de criacao
        '''
        backup_existe = False

        arquivo = self._get_path_abs_backup()
        #arquivo existe?
        arquivo_existe = os.path.isfile(arquivo)
        #foi criado na data de hoje?
        if arquivo_existe:
            data_hoje = datetime.datetime.now().strftime('%d/%m/%Y')
            arquivo_stat = os.stat(self._get_path_abs_backup())
            arquivo_data_criacao = datetime.datetime.fromtimestamp(arquivo_stat[stat.ST_CTIME])
            arquivo_data_str = arquivo_data_criacao.strftime('%d/%m/%Y')

            if arquivo_data_str == data_hoje:
                backup_existe = True

        return backup_existe

    def get_info_arquivo_backup(self):
        '''
        Gerar a resposta com as definições do arquivo: md5, tamanho e data criação para resposta
        '''
        resultado = None
        arquivo_path = self._get_path_abs_backup()
        arquivo_existe = os.path.isfile(arquivo_path)

        if arquivo_existe:
            nome = self._get_format_nome()
            path = self._backup.path_destino
            #data de criação
            arquivo_stat = os.stat(arquivo_path)
            arquivo_size = arquivo_stat[stat.ST_SIZE]
            time_stamp = arquivo_stat[stat.ST_CTIME]
            data_criacao = datetime.datetime.fromtimestamp(time_stamp)
            #hash verificação
            md5 = Gerar_md5().get_md5(arquivo_path)

            resultado = Arquivo(nome, path, md5, data_criacao, arquivo_size)

        return resultado

    def verifica_integridade_config(self):
        '''
        Teste valores do arquivo de configuracao backup_list.json
        futuramento mudar isso para o arquivo config
        '''
        resultato = False
        if self._backup.tipo == 'arquivo':
            resultado = os.path.isfile(self._get_path_abs_origem())
        elif self._backup.tipo == 'diretorio':
            resultado = os.path.isdir(self._backup.path_origem)

        resultado = os.path.isdir(self._backup.path_destino)
        '''
        #scripts nao estao funcionando
        if self._backup.backup_auto == 'Sim' and self._backup.backup_auto != '':
            resultado = os.path.isfile(self._backup.sc_backup)
        if self._backup.sc_pre_execucao != '':
            resultado = os.path.isfile(self._backup.sc_pre_execucao)
        if self._backup.sc_pos_execucao != '':
            resultado = os.path.isfile(self._backup.sc_pos_execucao)
        '''
        hora_execucao = Conv_data.str_to_time(self._backup.hora_execucao)
        if hora_execucao == None:
            resultado = False

        if not resultado:
            Log.log(logging.ERROR, 'Configuracao do {} esta incorreta'.format(self._backup.nome))

        return resultado

    def _get_path_abs_backup(self):

        if self._config.os_system() == 'Windows':
            path = self._backup.path_destino + '\\' + self._get_format_nome()
        else:
            path = self._backup.path_destino + '/' + self._get_format_nome()

        return path

    def _get_path_abs_origem(self):

        if self._config.os_system() =='Windows':
            path = self._backup.path_origem + '\\' + self._backup.fonte
        else:
            path = self._backup.path_origem + '/' + self._backup.fonte

        return path

    def _get_format_nome(self):
        nome_arquivo = self._backup.nome
        posfixo = Backup.dict_dia_semana[datetime.datetime.today().weekday()] + '_' + self._backup.hora_execucao.replace(':','')
        nome_completo = nome_arquivo + '_' + posfixo + '.zip'

        return nome_completo

    def _is_hora_exec(self, hora):
        t = datetime.datetime.now()
        minutes_now = self._hora_para_minutos(t)

        minutes_bkp = self._hora_para_minutos(hora)

        return (minutes_now >= minutes_bkp)

    def _hora_para_minutos(self, hora):
        temp = datetime.time(hour=hora.hour, minute=hora.minute)
        minutos = (temp.hour)*60 + (temp.minute)

        return minutos

    def _conv_hora(self, hora):
        return datetime.datetime.strptime(hora, '%H:%M')
