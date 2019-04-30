#!/usr/bin/env python3

import socket
import json

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 5000  # The port used by the server

data = {
    "comando":"desligar"
}
data_json = json.dumps(data)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(data_json.encode('utf-8'))
    data = s.recv(1024)

print("Received", repr(data))
