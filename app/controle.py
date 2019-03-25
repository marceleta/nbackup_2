
import config
import json

class Controle:

    def __init__(self):
        self.fim_conexao = 'fim'
        self.desligar_servidor = 'exit'
        self._mensage = ''
        self._data = bytes()
        self._config = config.Configuracao()

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
        print(type(data_json))
        lista = list()
        print(data_json['comando'])

        for d in data_json['lista']:
            lista.append(d)

        print('itens lista')
        for i in lista:
            print(i)


        #print(data_json['lista'][0])
        #print(data_json['lista'][1])



        #if self._processa_arquivo() == 'backup_list':
        #    print(self._config.get_backup())



    def enviar_resposta(self):
        return 'ok'.encode('utf-8')
