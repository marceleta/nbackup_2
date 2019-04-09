import datetime
import backup
import backup_zip
import arquivo
import util
import sys
from config import Configuracao
from abc import ABC, abstractmethod
import subprocess
import os, stat, time

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
    def get_arquivo_backup():
        pass



class Servico_diario(Template_servico):


    def __init__(self, backup):
        super.__init__(backup)
        self._backup = backup
        self._config = Configuracao()


    def verifica_execucao(self):
        is_executar = False
        lista_horario = self._backup['backup']['hora_execucao']

        for str_hora in lista_horario:
            _hora = self._conv_hora(str_hora)
            if self._is_hora_exec(_hora):
                self._hora_execucao = str_hora
                is_executar = True


        return is_executar

    def executar(self):
        self.executa_sc_pre()
        if self._backup.backup_auto == 'Sim':
            self.executa_sc_backup()
        else:
            self.executa_sc_nativo()
        self.executa_sc_pos()
        self.gerar_resposta()

    def executa_sc_pre(self):
        execucao = 'OK'
        str_sc = self._backup.sc_sc_execucao
        if str_sc == '':
            process = subprocess.Popen(str_sc, shell=True, stdout=subprocess.PIPE)
            output, erro = process.communicate()
            if erro not None:
                execucao = 'ERRO'

        return execucao

    def executa_sc_pos(self):
        execucao = 'OK'
        str_sc = self._backup.sc_pos_execucao
        if str_sc == '':
            process = subprocess.Popen(str_sc, shell=True, stdout=subprocess.PIPE)
            output, erro = process.communicate()
            if erro not None:
                execucao = 'ERRO'

        return execucao

    def executa_sc_backup(self):
        execucao = 'OK'
        str_sc = self._backup.sc_backup
        if str_sc == '':
            processo = subprocess.Popen(str_sc, shell=True, stdout=subprocess.PIPE)
            output, erro = processo.communicate()
            if erro not None:
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

    def get_arquivo_backup(self):
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
        posfixo = backup.Backup.dia_semana[datetime.datetime.today().weekday()] + "_" + self._hora_execucao.replace(':','')
        nome_completo = nome_arquivo + posfixo + '.zip'

        return nome_completo

    def _is_hora_exec(self, hora):
        t = datetime.datetime.now()
        minutes_now = super.hora_para_minutos(t)

        minutes_bkp = super.hora_para_minutos(hora)

        return (minutes_now >= minutes_bkp)


    def _conv_hora(self, hora):
        return datetime.datetime.strftime(hora, '%H:%M')
