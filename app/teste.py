import time, datetime
import modelos
import peewee

'''
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

try:
    zip = zipfile.ZipFile('teste.zip', mode='w')
    zip.write('/home/marcelo/ISO/hirens-bootcd-15-2-es-en-win.zip')
    zip.close()
    print('final')
except FileNotFoundError:
    print('FileNotFoundError')
except zipfile.BadZipfile:
    print('except BadZipfile')
except zipfile.LargeZipFile:
    print('except LargeZipFile')

'''

db = peewee.SqliteDatabase('nbackup.db')
db.connect()
#db.create_tables([modelos.Backup, modelos.Arquivo])

backup = modelos.Backup()
backup.tipo = 'arquivo'
backup.fonte = 'sql.dump'
backup._path_origem = '/home/marcelo/fonte'
backup.path_destino = '/home/marcelo/backup'
backup.periodo = 'diario'
backup.dia_semana = ''
backup.hora_execucao = '15:00'
backup.sc_pre_execucao = '/home/marcelo/script/script.sh'
backup.sc_pos_execucao = '/home/marcelo/script/script.sh'
backup.sc_backup = '/home/marcelo/script/backup.sh'
backup.backup_auto = 'Nao'
backup.create()

'''
arquivo = modelos.Arquivo()
arquivo.name = 'backup_1.zip'
arquivo.path = '/home/marcelo/backup'
arquivo.hash_verificacao = '123456d8f5g6e9d3s2d4d5f'
arquivo.data_criacao = datetime.datetime.now()
arquivo.backup = backup
arquivo.create()
'''
db.close()
