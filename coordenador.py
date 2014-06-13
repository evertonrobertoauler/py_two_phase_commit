import socket
from threading import Thread


class Coordenador:

    transaction = False
    server = None
    participantes = {}
    connection = {}

    def __init__(self):
        self.start_server_socket()

        # executa self.accept_connections em uma thread
        self.connection['thread'] = Thread(target=self.accept_connections)
        self.connection['thread'].start()

    def stop(self):
        self.test_transaction(False)

    def start_server_socket(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((socket.gethostname(), 4000))
        self.server.listen(10)

    def accept_connections(self):
        while True:
            (client, address) = self.server.accept()

            address = ":".join([str(a) for a in address])

            client.send(bytes("accepted", "UTF-8"))

            # executa self.receive(address, client) em uma thread
            thread = Thread(target=self.receive, args=(address, client))
            thread.start()

            self.participantes[address] = {
                'socket': client,
                'thread': thread
            }

    def receive(self, address, participante):
        while True:
            try:
                message = participante.recv(1024)
                if not message:
                    raise ConnectionResetError
                print('receive', message)

            except ConnectionResetError:
                if address in self.participantes:
                    del self.participantes[address]

    def send(self, address, message):
        if address in self.participantes:
            participante = self.participantes[address]['socket']

            try:
                participante.send(bytes(message, "UTF-8"))
            except ConnectionResetError:
                if address in self.participantes:
                    del self.participantes[address]

    def test_transaction(self, value=True):
        if self.transaction != value:
            if self.transaction:
                raise Exception("Transação já iniciada, finalize primeiro.")
            else:
                raise Exception("Transação não iniciada.")

    def begin_transaction(self):
        self.test_transaction(False)
        self.transaction = True

    def creditar(self, address, valor):
        self.test_transaction()
        self.send(address, "creditar(%f)" % valor)
        print('send', address, "'creditar(%f)'" % valor)

    def debitar(self, address, valor):
        self.test_transaction()
        self.send(address, "debitar(%f)" % valor)
        print('send', address, "'debitar(%f)'" % valor)

    def finish_transaction(self):
        self.test_transaction()
        self.transaction = False