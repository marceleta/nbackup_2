from peewee import *

db = SqliteDatabase('db/nbackup.db')

class BaseModel(Model):
    class Meta:
        database = db

class Backup(BaseModel):


    tipo = CharField()
    fonte = CharField()
    path_origem = CharField()
    path_destino = CharField()
    periodo = CharField()
    dia_semana = CharField()
    hora_execucao = CharField()
    sc_pre_execucao = CharField()
    sc_pos_execucao = CharField()
    sc_backup = CharField()
    backup_auto = CharField()

    def _format_hora(self, hora):
        h = datetime.datetime.strptime(hora,'%H:%M')

        return h


class Arquivo(BaseModel):

    nome = CharField()
    path = CharField()
    hash_verificacao = CharField()
    data_criacao = CharField()
    backup = ForeignKeyField(Backup, backref='backup')
