#!/usr/bin/env python3
from registro.registro import Registro
from configuracao.config import Configuracao
from servidor.server import SelectorServer

Registro.criar_banco()
config = Configuracao()
config_server = config.get_server_config()

server = SelectorServer('localhost', 5000, 5)
server.run_server()
