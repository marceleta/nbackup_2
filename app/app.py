#!/usr/bin/env python3

import time

from config import Configuracao
from server import SelectorServer


def is_teste():

    return True

config = Configuracao()
config_server = config.get_server_config()

server = SelectorServer(config_server.host, config_server.porta,
                        config_server.qtd_conecoes)
server.run_server()
print(type(is_teste()))
print(type(server.is_data()))
while True:
    if server.is_data():
        print("is data")
        #server.send_message("funfou")
    else:
        print("no data")
    time.sleep(5)
