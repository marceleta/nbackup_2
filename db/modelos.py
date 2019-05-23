from peewee import *
import datetime

db = SqliteDatabase('/home/marcelo/python/nbackup/db/nbackup.db')



class BaseModel(Model):
    class Meta:
        database = db

class Backup(BaseModel):

    nome = CharField()
    tipo = CharField()
    backup_auto = CharField(null=True)
    tempo_execucao = FloatField(null=True)
    data_execucao = DateTimeField()
    #fonte = CharField()
    #path_origem = CharField()
    #path_destino = CharField()
    periodo = CharField()
    dia_semana = CharField()
    hora_execucao = DateTimeField()
    sc_pre_execucao = CharField(null=True)
    sc_pos_execucao = CharField(null=True)
    sc_backup = CharField(null=True)

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
    tamanho = FloatField()
    is_enviado = BooleanField(default=False)
    data_envio = DateTimeField(null=True)
    backup = ForeignKeyField(Backup, backref='backup')

    @staticmethod
    def get_nao_enviados():
        arquivos = Arquivo.select().where(Arquivo.is_enviado==False)

        return arquivos

    @staticmethod
    def set_enviado(id):
        lista = Arquivo.select().where(Arquivo.id==id)
        for arquivo in lista:
            arquivo.is_enviado = True
            arquivo.data_envio = datetime.datetime.now()
            arquivo.save()


    def get_dict(self):
        d = {
            'id':id,
            'nome':nome,
            'path':path,
            'hash_verificacao':hash_verificacao,
            'data_criacao':data_criacao,
            'tamanho':tamanho,
            'is_enviado':is_enviado,
            'backup_id':backup
        }

        return d
