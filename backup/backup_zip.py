
import zipfile
import datetime
import os
import stat
from util.util import Log

class Backup_zip:


    def __init__(self, tipo, path_origem, path_destino, os):
        '''
        Definições:
        tipo = arquivo ou _zip_diretorio
        path_origem = path absoluto do diretorio ou arquivo para backup
        path_destino = nome final do arquivo a ser gerado o zip com o path
        os = sistema operacional
        '''
        self._tipo = tipo
        self._path_origem = path_origem
        self._path_destino = path_destino
        self._os = os

    def zip_backup(self):
        resultado = ''
        if self._tipo == 'arquivo':
            resultado = self._zip_arquivo()
        else:
            resultado = self._zip_diretorio()

        return resultado



    def _zip_arquivo(self):
        resultado = 'erro: '
        try:
            zip = zipfile.ZipFile(self._path_destino, mode='w', allowZip64=True)
            zip.write(self._path_origem, compress_type=zipfile.ZIP_DEFLATED)
            Log.info('zipando arquivo: {}'.format(self._path_destino))
            zip.close()
            resultado = 'sucesso'
        except FileNotFoundError:
            Log.error('erro zip arquivo:{} erro: {}'.format(self._path_destino, 'FileNotFoundError'))
            resultado = resultado + 'FileNotFoundError'
        except zipfile.BadZipfile:
            resultado = resultado + 'BadZipfile'
            Log.error('erro zip arquivo:{} erro: {}'.format(self._path_destino, 'BadZipfile'))
        except zipfile.LargeZipFile:
            resultado = resultado + 'LargeZipFile'
            Log.error('erro zip arquivo:{} erro: {}'.format(self._path_destino, 'LargeZipFile'))

        return resultado
       
    def _zip_diretorio(self):
        lista_arquivos = []
        resultado = 'erro: '
        for root, dirs, files in os.walk(self._path_origem):
            for file_name in files:
                lista_arquivos.append(file_name)

            try:
                zip = zipfile.ZipFile(self._path_destino, mode='w', allowZip64=True)
                for file in lista_arquivos:
                    if self._os == 'Windows':
                        arquivo = self._path_origem + '\\' + file
                    else:
                        arquivo = self._path_origem + '/' + file

                    zip.write(arquivo, compress_type=zipfile.ZIP_DEFLATED)

                zip.close()
                resultado = 'sucesso'

            except FileNotFoundError:
                resultado = resultado + 'FileNotFoundError'
                Log.error('erro zip diretorio:{} erro: {}'.format(self._path_destino, 'LargeZipFile'))
            except zipfile.BadZipfile:
                resultado = resultado + 'BadZipfile'
                Log.error('erro zip diretorio:{} erro: {}'.format(self._path_destino, 'BadZipfile'))
            except zipfile.LargeZipFile:
                resultado = resultado + 'LargeZipFile' 
                Log.error('erro zip diretorio:{} erro: {}'.format(self._path_destino, 'LargeZipFile'))        
