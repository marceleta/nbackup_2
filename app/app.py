#!/usr/bin/env python3

import time

import config
import server


def is_teste():

    return True

config = config.Configuracao()
config_server = config.get_server_config()

server = server.SelectorServer(config_server.host, config_server.porta,
                        config_server.qtd_conecoes)
server.run_server()
'''
print(type(is_teste()))
print(type(server.is_data()))
while True:
    if server.is_data():
        print("is data")
    else:
        print("no data")
    time.sleep(5)
'''
