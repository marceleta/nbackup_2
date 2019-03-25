import socket
import selectors
import logging
import time
import threading

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

class Conecoes:

    def __init__(self, id, conn):
        self._id = id
        self._conn = conn

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, id):
        self._id = id

    @property
    def conn(self):
        return self._conn

    @conn.setter
    def conn(self, conn):
        self._conn = conn

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
        self.conexoes = []
        self.index = 0


    def on_accept(self, sock, mask):
        self.index = self.index + 1
        conn, addr = self.main_socket.accept()
        logging.info('accepted connection from {0}'.format(addr))
        conn.setblocking(False)

        self.current_peers[conn.fileno()] = conn.getpeername()
        conexao = Conecoes(self.index, conn)
        self.conexoes.append(conexao)
        self.selector.register(fileobj=conn, events=selectors.EVENT_READ,
                                data=self.on_read)

    def on_read(self, conn, mask):
        try:
            data = conn.recv(1024)
            if data:
                logging.info('recebi dados de: {}'.format(conn.getpeername()))
            else:
                self.remove_conn(conn)
                self.close_connection(conn)

        except ConnectionResetError:
            self.remove_conn(conn)
            self.close_connection(conn)

    def remove_conn(self, conn):
        for conexao in self.conexoes:
            if conexao.conn == conn:
                del self.conexoes[conexao]

    def is_data(self):
        is_data = False

        for conexao in self.conexoes:
            data = conexao.conn
            if data:
                is_data = True
            else:
                is_data = False

        return is_data

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
            logging.info('An event occurred')

            for key, mask in events:
                handler = key.data
                handler(key.fileobj, mask)


            cur_time = time.time()

            if cur_time - last_report_time > 1:
                logging.info('Running report...')
                logging.info('Num active peers = {0}'.format(
                                len(self.current_peers)))
                last_report_time = cur_time


    def run_server(self):
        self.thread = threading.Thread(target=self.serve_forever)
        self.thread.start()
