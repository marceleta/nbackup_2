from configuracao.config import Configuracao

config = Configuracao()

for backup in config.get_backups():
    print(backup.nome)
