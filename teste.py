from configuracao.config import Configuracao

config = Configuracao()

for backup in config.get_backups():
    print(backup.nome)

for usuario in config.get_usuarios():
    print(usuario.usuario)

servidor = config.get_server_config()
ftp = servidor.config_ftp()

print(ftp.host)
