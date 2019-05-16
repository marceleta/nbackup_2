import datetime

from db.modelos import Backup, Arquivo
from util.util import Conv_data
from configuracao.config import Configuracao

class Registro:
    def __init__(self, backup, resultado_execucao, tempo_execucao=None, arquivo=None):
        self._arquivo = arquivo
        self._backup = backup
        self._resultado_execucao = resultado_execucao
        self._tempo_execucao = tempo_execucao

    def registrar(self):
        mbackup = Backup()
        mbackup.nome = self._backup.nome
        mbackup.tipo = self._backup.tipo
        mbackup.data_execucao = Conv_data.get_date_now()
        mbackup.periodo = self._backup.periodo
        if self._tempo_execucao != None:
            mbackup.tempo_execucao = self._tempo_execucao
        mbackup.dia_semana = self._backup.dia_semana
        split_hora = self._backup.hora_execucao.split(':')
        int_hora = int(split_hora[0])
        int_minutos = int(split_hora[1])
        _hora_execucao = datetime.time(hour=int_hora, minute=int_minutos)
        mbackup.hora_execucao = _hora_execucao
        mbackup.sc_pre_execucao = self._resultado_execucao['executa_sc_pre']
        mbackup.sc_pos_execucao = self._resultado_execucao['executa_sc_pos']
        mbackup.backup_auto = self._backup.backup_auto
        if self._backup.backup_auto == 'Sim':
            mbackup.sc_backup = self._resultado_execucao['executa_backup_auto']
        else:
            mbackup.sc_backup = self._resultado_execucao['executa_sc_nativo']

        mbackup.save()

        if self._arquivo != None:
            m_arquivo = Arquivo()
            m_arquivo.nome = self._arquivo.nome
            m_arquivo.path = self._arquivo.path
            m_arquivo.hash_verificacao = self._arquivo.hash_verificacao
            m_arquivo.data_criacao = self._arquivo.data_criacao
            m_arquivo.tamanho = self._arquivo.tamanho
            m_arquivo.backup = mbackup

            m_arquivo.save()

    @staticmethod
    def criar_banco():
        try:
            if Configuracao.os_system() == 'Windows':
                path_db = 'c:/nbackup/db/nbackup.db'
            else:
                path_db = '/home/marcelo/python/nbackup/db/nbackup.db'

            arquivo = open(path_db)
        except FileNotFoundError:
            Backup.create_table()
            Arquivo.create_table()
