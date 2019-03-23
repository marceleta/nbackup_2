import socket
import selectors
import logging
import time

logging.basicConfig(filename='nbackup.log', filemode='a', level=logging.INFO, format='[%(asctime)s %(message)s]')

class Server():

    def __init__(self, host, porta, qtd_conecoes):
        self._host = host
        self._porta = porta
        self._qtd_conecoes = qtd_conecoes


    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        self._host = value

    @property
    def porta(self):
        return self._porta

    @porta.setter
    def porta(self, value):
        self._porta = value

    @property
    def qtd_conecoes(self):
        return self._qtd_conecoes

    @qtd_conecoes.setter
    def qtd_conecoes(self, value):
        self._qtd_conecoes = value

class SelectorServer:

    def __init__(self, host, port, listen):
        self.main_socket = socket.socket()
        self.main_socket.bind((host, port))
        self.main_socket.listen(100)
        self.main_socket.setblocking(False)


        self.selector = selectors.DefaultSelector()
        self.selector.register(fileobj=self.main_socket,
                                events=selectors.EVENT_READ,
                                data=self.on_accept)

        self.current_peers = {}
        self.current_peer = int()
        self.data_peers ={}


    def on_accept(self, sock, mask):
        conn, addr = self.main_socket.accept()
        logging.info('accepted connection from {0}'.format(addr))
        conn.setblocking(False)

        self.current_peers[conn.fileno()] = conn.getpeername()
        self.current_peer = conn.fileno()

        self.selector.register(fileobj=conn, events=selectors.EVENT_READ,
                                data=self.on_read)

    def on_read(self, conn, mask):

        try:
            self.data_peers[self.current_peer] = conn.recv(1024)
            if data:
                self.is_data = True
                peername = conn.getpeername()
                logging.info('got data from {}: {!r}'.format(peername, data))
                #conn.send(data)
            else:
                self.close_connection(conn)

        except ConnectionResetError:
                self.close_connection(conn)

    def get_message(self, index=0):
        print(index)
        i = int(index)
        if i == 0:
            data = self.data_peers[self.current_peer]
        else:
            data = self.data_peers[index]

        return data.decode('utf-8')

    def delete_data(self, index):
        i = int(index)
        if i == 0:
            data = self.data_peers[self.current_peer]
        else:
            data = self.data_peers[index]

        del data[0:]

    def get_is_data(self, index):
        i = int(index)
        for data in self.current_peers:
            if not data:
                is_data = False

        return is_data


    def send_message(self, message, index="0", close="False"):
        i = int(index)
        c = bool(close)
        data_bytes = message.encode('utf-8')
        if i == 0:
            conn = self.current_peers[self.current_peer]
            conn.send(data_bytes)

        if close:
            try:
                self.close_connection(conn)

            except ConnectionResetError:
                self.close_connection(conn)

    def close_connection(self, conn):

        peername = self.current_peers[conn.fileno()]
        logging.info('closing connection to {0}'.format(peername))
        del self.current_peers[conn.fileno()]
        self.selector.unregister(conn)
        conn.close()

    def serve_forever(self):
        last_report_time = time.time()

        while True:

            events = self.selector.select(timeout=0.2)

            for key, mask in events:
                handler = key.data
                handler(key.fileobj, mask)
                type(handler)

            cur_time = time.time()

            if cur_time - last_report_time > 1:
                logging.info('Running report...')
                logging.info('Num active peers = {0}'.format(
                                len(self.current_peers)))
                last_report_time = cur_time
