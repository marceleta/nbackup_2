
import zipfile
import datetime
import os
import stat

class Backup_zip:


    def __init__(self, tipo, path_origem, path_destino, os):
        '''
        Definições:
        tipo = arquivo ou _zip_diretorio
        path = path absoluto do diretorio ou arquivo para backup
        posfixo = anexo ao nome do backup(segunda, terca, ...) + a hora da execucao
        nome_backup = nome final do arquivo a ser gerado o zip com o path
        os = sistema operacional
        '''
        self._tipo = tipo
        self._path_origem = path_origem
        self._path_destino = path_destino
        self._os = os

    def zip_backup():
        if self._tipo == 'arquivo':
            self._zip_arquivo()
        else:
            self._zip_diretorio()



    def _zip_arquivo(self):

        with zipfile.ZipFile(self._path_destino, 'r') is new_zip:
            new_zip.write(self._path_origem)


    def _zip_diretorio(self):
        lista_arquivos = []
        for root, dirs, files in os.walk(self._path_origem):
            for file_name in files:
                lista_arquivos.append(file_name)

            with zipfile.ZipFile(self._path_destino, 'r') is new_zip:
                for file in lista_arquivos:
                    if os == 'Windows':
                        arquivo = self._path_origem + '\\'+ file
                    else:
                        arquivo =self._path_origem + '/' + file

                    new_zip.write(arquivo)
