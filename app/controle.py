
import config
import json
import backup
import servico
import util
import threading
import time

class Controle:

    def __init__(self):
        self._fim_conexao = 'fim'
        self._desligar_servidor = 'desligar_servidor'
        self._cmd_desligar = False
        self._mensage = ''
        self._data = bytes()
        self._config = config.Configuracao()
        self._bkp_conversor = backup.Backup_dict()
        self._thread_servico = True


    def set_data(self, data):
         self._data = data
         self._decode_data(self._data)

    def _decode_data(self, data):
        if data:
            self._mensagem = data.decode('utf-8')

    def is_data(self):
        is_data = True
        if not self._data:
            is_data = False

        return is_data


    def processar_mensagem(self):
        data_json = json.loads(self._data.decode('utf-8'))
        comando = data_json['comando']
        print('Comando: {}'.format(comando))

        if comando == 'bkp_list':
            self._resposta = self._lista_backups()

        elif comando == 'add_bkp':
            bkp_para_add = data_json['bkp_list_add']
            self._resposta = self._add_backup(bkp_para_add)

        elif comando == 'list_bkp_prontos':
            self._resposta = self._backups_prontos()

        elif comando == 'iniciar_ftp':
            self._resposta = self._iniciar_ftp()

        elif comando == self._desligar_servidor:
            self._resposta = self.get_shutdown()
            self._cmd_desligar = True

        else:
            self._resposta == "comando_nao_encontrado"


    def _lista_backups(self):
        list_backup = self._config.get_backups()
        size_list = len(list_backup)
        list_str = []
        for i in range(size_list):
            list_str.append(list_backup[i].get_dict())

        backup_json = json.dumps(list_str)

        return backup_json.encode('utf-8')

    def _add_backup(self, lista_para_add):
        pass

    def _backups_prontos(self):
        pass

    def _iniciar_ftp(self):
        pass

    def _iniciar_thread_servicos(self):
        self._thread_servico = True
        thread = threading.Thread(target=self._verifica_servicos)
        thread.start()

    def _verifica_servicos(self):
        while self._thread_servico:
            for servico in self._criar_lista_servicos():
                if servico.verifica_execucao():
                    self._exec_serv_thread(servico)
            time.sleep(1000)

    def _exec_serv_thread(self, servico):
        thread = threading.Thread(target=servico.executar())
        thread.start()


    def _criar_lista_servicos(self):
        lista_backup =self._config.get_backups()
        lista_servico = []
        for backup in lista_backup:
            if backup.periodo == 'diario':
                servico_diario = servico.Servico_diario(backup)
                lista_servico.append(servico_diario)

        return lista_servico


    def get_shutdown(self):
        return 'desligando'.encode('utf-8')

    def get_running(self):

        print(not self._cmd_desligar)
        return not self._cmd_desligar

    def enviar_resposta(self):
        return self._resposta
