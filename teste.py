from configuracao.config import Configuracao
from ftp.servidor_ftp import Ftp_thread, Servidor_ftp, Gestao_ftp
import time

#config = Configuracao()

info = {'path':'/home/marcelo/backup/backup1','nome':'backup_1_segunda_0745.zip','backup':'backup_1'}
print(info['path'])

#thread = Ftp_thread(config.get_server_config().config_ftp(), '/home/marcelo/backup/backup1', 'backup_1')
#thread.start()

gestao_ftp = Gestao_ftp()
resposta = gestao_ftp.adicionar(info)
contador = 0
loop = True
while loop:
    print('em andamento: {}'.format(gestao_ftp.get_em_andamento()))

    if contador == 5:
        print('fim ftp')
        resultado = gestao_ftp.desligar(info['backup'])
        print('is_desligado: {}'.format(resultado))

    if contador == 10:
        print('fim loop')
        loop = False

    contador += 1

    time.sleep(6)
    
