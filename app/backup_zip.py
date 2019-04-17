
import zipfile
import datetime
import os
import stat

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
            zip.write(self._path_origem)
            zip.close()
            resultado = 'sucesso'
        except FileNotFoundError:
            resultado = resultado + 'FileNotFoundError'
        except zipfile.BadZipfile:
            resultado = resultado + 'BadZipfile'
        except zipfile.LargeZipFile:
            resultado = resultado + 'LargeZipFile'

        return resultado


        '''
        with zipfile.ZipFile(self._path_destino, 'w') as new_zip:
            new_zip.write(self._path_origem)
        '''


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

                    zip.white(arquivo)

                zip.close()
                resultado = 'sucesso'

            except FileNotFoundError:
                resultado = resultado + 'FileNotFoundError'
            except zipfile.BadZipfile:
                resultado = resultado + 'BadZipfile'
            except zipfile.LargeZipFile:
                resultado = resultado + 'LargeZipFile'

            '''
            with zipfile.ZipFile(self._path_destino, 'w') as new_zip:
                for file in lista_arquivos:
                    if self._os == 'Windows':
                        arquivo = self._path_origem + '\\'+ file
                    else:
                        arquivo =self._path_origem + '/' + file

                    new_zip.write(arquivo)
            '''
