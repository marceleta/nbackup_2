from config import Configuracao
from servidor_ftp import Gestao_ftp
from threading import Thread
import time

'''
print('olamundo')

authorizer = DummyAuthorizer()
authorizer.add_user("user","12345","/home/marcelo/ftp",perm="elradfmw")
#authorizer.add_anonymous("/home/marcelo/ftp", perm="elradfmw")

handler = FTPHandler
handler.authorizer = authorizer

server = FTPServer(("localhost", 5000), handler)
print('pre server')
server.serve_forever()
'''

'''
config = Configuracao()
config_ftp = config.get_config_ftp()
servidor_ftp = Servidor_ftp(config_ftp,'/home/marcelo/ftp')
thread = Ftp_thread(servidor_ftp)
thread.start()
'''

ftp = Gestao_ftp('/home/marcelo/ftp', 'backup_1')
ftp.iniciar()
contador = 0
while contador <= 20:
    print('nome: {}'.format(ftp.get_nome()))
    print('is_alive: {}'.format(ftp.is_ativo()))
    time.sleep(3)
    contador = contador + 1
    if contador == 10:
        print('desligando ftp')
        ftp.desligar()


print('is_alive: {}'.format(ftp.is_ativo()))
print('fim')
