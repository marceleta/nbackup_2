#!/usr/bin/env python3

import time

import config
import server


config = config.Configuracao()
config_server = config.get_server_config()

server = server.SelectorServer(config_server.host, config_server.porta,
                        config_server.qtd_conecoes)
server.run_server()
