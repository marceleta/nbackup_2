from peewee import *
import datetime

db = SqliteDatabase('db/nbackup.db')



class BaseModel(Model):
    class Meta:
        database = db

class Backup(BaseModel):

    nome = CharField()
    tipo = CharField()
    tempo_execucao = FloatField()
    data_execucao = DateTimeField()
    #fonte = CharField()
    #path_origem = CharField()
    #path_destino = CharField()
    periodo = CharField()
    dia_semana = CharField()
    hora_execucao = DateTimeField()
    sc_pre_execucao = CharField()
    sc_pos_execucao = CharField()
    sc_backup = CharField()
    sc_backup_auto = CharField()

    @staticmethod
    def is_backup_executado(nome, data_execucao, hora_execucao):
        '''
        verifica se o backup(nome, data_execucao e hora_execucao) existe
        no banco de dados
        '''
        bkp = None
        try:
            bkp = Backup.get(Backup.nome==nome,
                            Backup.data_execucao==data_execucao,
                            Backup.hora_execucao==hora_execucao)
        except DoesNotExist:
                bkp = None

        return bkp



    def hora(self):
        h = datetime.datetime.strptime(hora_execucao,'%H:%M')
        return h

    def _format_hora(self, hora):
        h = datetime.datetime.strptime(hora,'%H:%M')

        return h


class Arquivo(BaseModel):

    nome = CharField()
    path = CharField()
    hash_verificacao = CharField()
    data_criacao = CharField()
    backup = ForeignKeyField(Backup, backref='backup')
