#!/usr/bin/env python3

import time

import config
import server


config = config.Configuracao()
config_server = config.get_server_config()

server = server.SelectorServer('localhost', 5000, 5)
server.run_server()
