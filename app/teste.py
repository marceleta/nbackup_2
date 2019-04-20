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

db = peewee.SqliteDatabase('db/nbackup.db')
db.create_tables([modelos.Backup, modelos.Arquivo])

'''
backup = modelos.Backup()
backup.nome = 'backup_1'
backup.tipo = 'arquivo'
backup.fonte = 'sql.dump'
backup.path_origem = '/home/marcelo/fonte'
backup.path_destino = '/home/marcelo/backup'
backup.periodo = 'diario'
backup.dia_semana = ''
hora = datetime.time(hour=15, minute=30)
backup.hora_execucao = hora
backup.sc_pre_execucao = '/home/marcelo/script/script.sh'
backup.sc_pos_execucao = '/home/marcelo/script/script.sh'
backup.sc_backup = '/home/marcelo/script/backup.sh'
backup.backup_auto = 'Nao'
backup.save()

arquivo = modelos.Arquivo()
arquivo.nome = 'backup_1.zip'
arquivo.path = '/home/marcelo/backup'
arquivo.hash_verificacao = '123456d8f5g6e9d3s2d4d5f'
arquivo.data_criacao = datetime.datetime.now()
arquivo.backup = backup
arquivo.save()
'''
'''
bks = modelos.Backup.select()
for b in bks:
    print('nome: {}'.format(b.nome))
    print('hora_execucao: {}'.format(b.hora_execucao))
    #print('type hora: {}'.format(type(b.hora())))

a1 = modelos.Arquivo().select()

for arquivo in a1:
    print('nome backup: {}'.format(arquivo.backup.nome))
    print('path: {}'.format(arquivo.path))
'''
