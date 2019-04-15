import datetime
import backup
import backup_zip
import arquivo
import util
import sys
import config
from abc import ABC, abstractmethod
import subprocess
import os, stat, time
import threading
from threading import Thread

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
        Thread.__init__(self, name=servico.get_nome())
        self._servico = servico
        self._inicio = None
        self._final = None
        self._resultado = None

        def run():
            self._resultado = self._servico.executar()

    def get_resultado(self):
        '''
        Retorna None se não houver resultado,
        retorna um dict caso haja um resultado
        '''
        self._resultado


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
        self._config = config.Configuracao()

    def get_nome(self):
        return self._backup.nome


    def verifica_execucao(self):
        is_executar = False
        lista_horario = self._backup.hora_execucao

        for str_hora in lista_horario:
            _hora = self._conv_hora(str_hora)
            if self._is_hora_exec(_hora):
                self._hora_execucao = str_hora
                print('hora_execucao: {}'.format(self._hora_execucao))
                is_executar = True


        return is_executar

    def executar(self):
        dict_resultado = {}

        resultado = self.executa_sc_pre()
        dict_resultado['executa_sc_pre'] = resultado

        if self._backup.backup_auto == 'Sim':
            resultado = self.executa_sc_backup()
            dict_resultado['executa_backup_auto'] = resultado
        else:
            resultado = self.executa_sc_nativo()
            dict_resultado['executa_sc_nativo'] = resultado

        resultado = self.executa_sc_pos()
        dict_resultado['executa_sc_pos'] = resultado

        return dict_resultado


    def executa_sc_pre(self):
        execucao = 'OK'
        str_sc = self._backup.sc_sc_execucao
        if str_sc == '':
            process = subprocess.Popen(str_sc, shell=True, stdout=subprocess.PIPE)
            output, erro = process.communicate()
            if erro == None:
                execucao = 'ERRO'

        return execucao

    def executa_sc_pos(self):
        execucao = 'OK'
        str_sc = self._backup.sc_pos_execucao
        if str_sc == '':
            process = subprocess.Popen(str_sc, shell=True, stdout=subprocess.PIPE)
            output, erro = process.communicate()
            if erro == None:
                execucao = 'ERRO'

        return execucao

    def executa_sc_backup(self):
        execucao = 'OK'
        str_sc = self._backup.sc_backup
        if str_sc == '':
            processo = subprocess.Popen(str_sc, shell=True, stdout=subprocess.PIPE)
            output, erro = processo.communicate()
            if erro == None:
                execucao = 'ERRO'

        return execucao

    def executa_sc_nativo(self):

        if self._backup.tipo == 'arquivo':
            path_origem = self._get_path_abs_origem()
        else:
            path_origem = self._backup.path_origem

        backup_zip = backup_zip.Backup_zip(self._backup.tipo, path_origem,
                                            self._get_path_abs_backup, self._config.os_system())

        backup_zip.zip_backup()


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
            data_hoje = datetime.datetime.now().strftime('%d/%m%/%Y')
            arquivo_backup = os.stat(self._get_path_abs_backup())
            data_arquivo = time.strftime('%d/%m/%Y', time.localtime(arquivo_backup[stat.ST_CTIME]))
            if data_arquivo == data_hoje:
                backup_existe = True

        return backup_existe

    def get_info_arquivo_backup(self):
        '''
        Gerar a resposta com as definições do arquivo: md5, tamanho e data criação para resposta
        '''
        arquivo = self._get_path_abs_backup()

        nome = self._get_format_nome()
        path = self._backup.path_destino
        #data de criação
        arquivo_stat = os.stat(arquivo)
        arquivo_size = arquivo_stat[stat.ST_SIZE]
        date = arquivo_stat[stat.ST_CTIME]
        f_data = time.strftime('%d/%m/%Y %H:%M:%S', date)
        #hash verificação
        md5 = util.Gerar_md5().get_md5(arquivo)

        arquivo = arquivo.Arquivo(nome, path, md5, f_data)

        return arquivo



    def _get_path_abs_backup(self):

        if self._config.os_system() == 'Windows':
            path = self._backup.path_destino + "\\" + self._get_format_nome()
        else:
            path = self._backup.path_destino + "/" + self._get_format_nome()

        return path

    def _get_path_abs_origem(self):

        if self._config.os_system() =='Windows':
            path = self._backup.path_origem + '\\' + self._backup.fonte
        else:
            path = self._backup.path_origem + '/' + self._backup.fonte

    def _get_format_nome(self):
        nome_arquivo = self._backup.nome
        print('hora_execucao: {}'.format(self._hora_execucao))
        posfixo = backup.Backup.dia_semana[datetime.datetime.today().weekday()] + '_' + self._hora_execucao.replace(':','')
        nome_completo = nome_arquivo + posfixo + '.zip'

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
