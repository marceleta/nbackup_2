
import servico
import config
import time
import sys


config = config.Configuracao()

lista_backups = config.get_backups()
dict_servicos = {}

for backup in lista_backups:
    s = servico.Servico_diario(backup)
    dict_servicos[backup.nome] = s

while True:

    for key in dict_servicos.keys():
        serv = dict_servicos[key]
        if serv.verifica_execucao():
            serv.executar()
            sys.exit()


    time.sleep(30)
