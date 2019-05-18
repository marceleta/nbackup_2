from configuracao.config import Configuracao
from ftp.servidor_ftp import Ftp_thread, Servidor_ftp
import time

config = Configuracao()

thread = Ftp_thread(config.get_server_config().config_ftp(), '/home/marcelo/backup/backup1', 'backup_1')
thread.start()
while True:
    print('is_alive: {}'.format(thread.is_alive()))
    time.sleep(10)
