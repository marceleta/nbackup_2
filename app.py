#!/usr/bin/env python3
from registro.registro import Registro
from configuracao.config import Configuracao
from servidor.server import SelectorServer
from util.util import Log

Registro.criar_banco()
config = Configuracao()
config_server = config.get_server_config()

server = SelectorServer(config_server.host, config_server.porta, config_server.qtd_conexoes)
server.run_server()
Log.info('iniciando aplicacao')
