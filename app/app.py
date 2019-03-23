#!/usr/bin/env python3

from config import Configuracao
from server import SelectorServer

config = Configuracao()
config_server = config.get_server_config()

server = SelectorServer(config_server.host, config_server.porta,
                        config_server.qtd_conecoes)

server.serve_forever()
print("pos serve_forever")
