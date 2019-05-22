import json
import threading
import time
from configuracao.config import Configuracao
from json_modelos.modelos import Backup, Backup_dict
from servico.servico import Servico_diario, ServicoThread
from util.util import Conv_data, Conversor, Gerar_md5
from registro.registro import Registro
from ftp.servidor_ftp import Gestao_ftp
from db.modelos import Backup as Backup_db, Arquivo


class Controle:

    def __init__(self):
        self._fim_conexao = 'fim'
        self._cmd_desligar = False
        self._mensage = ''
        self._data = bytes()
        self._config = Configuracao()
        self._gestao_ftp = Gestao_ftp()
        self._bkp_conversor = Backup_dict()
        self._loop_controle = True
        self._thread_servico = {}
        self._thread_controle = {}
        self._threads_finalizados = {}
        self._threads_ftps = {}
        self._lista_bkp_executando = []
        self._verifica_servico = 'Verifica servicos'
        self._threads_ativos = 'Threads ativos'
        self._reg_serv_finalizados = 'Registra servicos'

        self._iniciar_thread_controle()


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
        data_json = json.loads(self._data)
        comando = data_json['comando']
        del data_json['comando']
        print('Comando: {}'.format(comando))
        print('data_json: {}'.format(data_json))

        if comando == 'bkp_list':
            self._resposta = self._lista_backups()

        elif comando == 'update_lst_bkp':
            self._resposta = self._atualizar_config_bkps(data_json)

        elif comando == 'list_bkps_prontos':
            self._resposta = self._backups_prontos()

        elif comando == 'iniciar_ftp':
            self._resposta = self._iniciar_ftp(data_json)

        elif comando == 'fechar_ftp':
            self._resposta = self._fechar_ftp(data_json)

        elif comando == 'desligar':
            self._resposta = 'desligando'
            self._desligar_servidor()

        elif comando == 'reiniciar':
            self._resposta = 'reiniciando servicos'
            self._reinicia_threads_controle()

        elif comando == 'teste':
            self._resposta = 'ok'

        else:
            self._resposta = "comando_nao_encontrado"

        self._data = None

    def _atualizar_config_bkps(self, comando):
        self._config.salvar_config_bkps(comando)
        resposta = {
            'resposta':'salvar_bkps_ok'
        }

        return json.dumps(resposta)

    def _lista_backups(self):
        list_backup = self._config.get_backups()
        size_list = len(list_backup)
        list_str = []
        for i in range(size_list):
            list_str.append(list_backup[i].get_dict())

        backup_json = json.dumps(list_str)

        return backup_json


    def _add_backup(self, lista_para_add):
        pass

    def _backups_prontos(self):
        arquivos = Arquivo.get_nao_enviados()
        lista_arquivos = []
        for arquivo in arquivos:
            d = {
            'id':arquivo.id,
            'arquivo':arquivo.nome,
            'path':arquivo.path,
            'hash_verificacao':arquivo.hash_verificacao,
            'data_criacao':arquivo.data_criacao,
            'tamanho':arquivo.tamanho,
            'backup':arquivo.backup.nome,
            'is_enviado':arquivo.is_enviado
            }
            lista_arquivos.append(d)


        resposta = {
            'resposta':'lst_bkps_prontos',
            'conteudo':lista_arquivos
        }

        print('_backup_prontos:resposta {}'.format(resposta))

        return json.dumps(resposta)


    def _iniciar_ftp(self, comando):
        if not self._gestao_ftp.is_rodando_ftp():
            resposta = self._gestao_ftp.adicionar(comando['backup'])
        else:
            resposta = {
                'resposta':'ftp_rodando',
                'conteudo':'ftp_ocupado'
            }

        print(resposta)

        return json.dumps(resposta)

    def _fechar_ftp(self, comando):
        is_desligado = self._gestao_ftp.desligar(comando['nome'])
        print('_fechar_ftp:is_desligado: {}'.format(is_desligado))
        str_id = comando['id_arquivo']
        id = int(str_id)
        Arquivo.set_enviado(id)

        resposta = {'resposta':'ok',
                    'conteudo':'download arquivo executado com sucesso'
                    }

        return json.dumps(resposta)


    def _iniciar_thread_controle(self):
        self._loop_controle = True

        thread_verificacao = threading.Thread(target=self._verifica_servicos, name=self._verifica_servico)
        self._thread_controle[self._verifica_servico] = thread_verificacao
        thread_verificacao.start()

        thread_ativos = threading.Thread(target=self._verifica_thread_ativos, name=self._threads_ativos)
        self._thread_controle[self._threads_ativos] = thread_ativos
        thread_ativos.start()

        thread_reg_finalizado = threading.Thread(target=self._registar_servicos_finalizados, name=self._reg_serv_finalizados)
        self._thread_controle[self._reg_serv_finalizados] = thread_reg_finalizado
        thread_reg_finalizado.start()

    def _reinicia_threads_controle(self):
        self._loop_controle = False
        time.sleep(65)
        self._config = Configuracao()
        self._iniciar_thread_controle()

    def _desligar_servidor(self):
        self._loop_controle = False
        time.sleep(65)
        self._cmd_desligar = True


    def _verifica_servicos(self):
        dict_servicos = self._criar_servicos_diario()
        print('dict_servicos: {}'.format(dict_servicos))
        while self._loop_controle:
            lista_nome_servicos = list(dict_servicos.keys())
            print('Lista nome servicos: {}'.format(lista_nome_servicos))
            for key in lista_nome_servicos:
                servico = dict_servicos[key]
                if servico.verifica_integridade_config():
                    if self._verifica_servico_executado(servico.get_backup()):
                        del dict_servicos[key]
                    elif servico.verifica_execucao():
                        self._add_servico_thread(servico)
                        del dict_servicos[key]
                else:
                    del dict_servicos[key]

                #servico = dict_servicos[key]
                #if servico.verifica_execucao():
                #    self._add_servico_thread(servico)
                #    del dict_servicos[key]

            time.sleep(60)

    def _verifica_servico_executado(self, backup):
        '''
        Verrifica se o backup já foi executado no dia corrente
        Caso o servidor seja reiniciado nao executar os servicos de backup novamente
        '''
        resultado = False
        data = Conv_data.get_date_now()
        hora = Conv_data.str_to_time(backup.hora_execucao)
        bkp = Backup_db.is_backup_executado(backup.nome, data, hora)

        if bkp != None:
            resultado = True

        return resultado


    def _add_servico_thread(self, serv):
        thread = ServicoThread(serv)
        self._thread_servico[serv.get_nome()] = thread
        thread.set_inicio_thread(time.time())
        thread.start()

    def _verifica_thread_ativos(self):
        while self._loop_controle:
            lista_thread_ativos = list(self._thread_servico.keys())
            print('lista_thread_ativos: {}'.format(lista_thread_ativos))
            for key in lista_thread_ativos:
                thread = self._thread_servico.get(key)
                print('verifica thread: {}'.format(thread.name))
                print('thread.is_alive: {}'.format(thread.is_alive()))
                if not thread.is_alive():
                    thread.set_final_thread(time.time())
                    self._threads_finalizados[thread.get_nome()] = thread
                    del self._thread_servico[key]

            time.sleep(60)

    def _registar_servicos_finalizados(self):
        # Registar no banco de dados
        #testar ate aqui
        while self._loop_controle:
            lista_finalizados = list(self._threads_finalizados.keys())
            print('lista_finalizados size: {}'.format(lista_finalizados))
            for key in lista_finalizados:
                thread = self._threads_finalizados[key]
                t_execucao = (thread.get_final_thread() - thread.get_inicio_thread())
                servico = thread.get_servico()
                backup = servico.get_backup()
                arq = None
                if servico.verifica_backup_existe():
                    arq = servico.get_info_arquivo_backup()

                self._registro = Registro(backup, servico.get_resultado(), tempo_execucao=t_execucao, arquivo=arq)
                self._registro.registrar()

                '''
                print('Nome servico: {}'.format(thread.get_nome()))
                print('Delta time: {}'.format(thread.get_final_thread() - thread.get_inicio_thread()))
                print('Resultado execucao: {}'.format(servico.get_resultado()))
                print('backup existe? {}'.format(servico.verifica_backup_existe()))
                arquivo = servico.get_info_arquivo_backup()
                print('Arquivo nome: {}'.format(arquivo.nome))
                print('Arquivo path: {}'.format(arquivo.path))
                print('Arquivo md5: {}'.format(arquivo.hash_verificacao))
                print('Arquivo data_criacao: {}'.format(arquivo.data_criacao))
                '''
                del self._threads_finalizados[key]

            time.sleep(60)




    #def _exec_serv_thread(self, servico):
    #    thread = threading.Thread(target=servico.executar())
    #    thread.start()


    def _criar_servicos_diario(self):
        lista_backup =self._config.get_backups()
        self._dict_servicos = {}
        for backup in lista_backup:
            if backup.periodo == 'diario':
                servico_diario = Servico_diario(backup)
                self._dict_servicos[backup.nome] = servico_diario

        return self._dict_servicos


    def get_shutdown(self):
        return 'desligando'.encode('utf-8')

    def get_running(self):
        return self._cmd_desligar

    def enviar_resposta(self):
        return self._resposta.encode('utf-8')
