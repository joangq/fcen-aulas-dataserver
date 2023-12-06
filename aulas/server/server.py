from logging import Logger

from aulas.logger import LoggerFactory, Colors
from socket import socket, AF_INET, SOCK_STREAM


class Server:
    log: Logger = LoggerFactory.getLogger('server')

    listeners = {
        "connection": [],
        "receive": []
    }

    socket: socket

    def __init__(self, port: int):
        self.host = '127.0.0.1'
        self.port = port

    def get_listeners(self, kind: str):
        listeners = self.listeners.get(kind, None)
        if listeners is None:
            raise Exception("Invalid listener kind. Valid kinds are: " + ', '.join(self.listeners.keys()))
        return listeners

    def add_listener(self, kind: str, listener: callable):
        self.get_listeners(kind).append(listener)

    def notify_listeners(self, kind: str, args: tuple):
        listeners = self.get_listeners(kind)
        if len(listeners) <= 0:
            return

        for listener in listeners:
            if isinstance(args, tuple):  # This is here because (*byte) returns an int.
                listener(*args)
            else:
                listener(args)

    def on_new_connection(self, connection, client_address):
        self.notify_listeners("connection", args=(connection, client_address))

    def on_receive_data(self, data):
        self.notify_listeners("receive", args=data)

    def start(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        self.log.info(f"Server listening on {self.host}:{self.port}")

        try:
            while True:
                connection, client_address = self.socket.accept()
                self.on_new_connection(connection, client_address)

                datalist: list[bytes] = []
                try:
                    while True:
                        data = connection.recv(1)  # 0 - 127
                        if not data:
                            break

                        datalist.append(data)
                        self.on_receive_data(data)
                        connection.sendall(data)
                except ConnectionResetError:
                    self.log.info("Connection was reset by peer.")
                    continue
                except Exception as e:
                    self.log.error(e)
                    raise e

                self.log.info(f"Received {len(datalist)} bytes of data.")
                connection.close()
        finally:
            self.socket.close()
            self.log.info(f"Server closed.")
