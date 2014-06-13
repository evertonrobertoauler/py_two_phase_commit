import socket
from threading import Thread
from json import JSONEncoder, JSONDecoder
import time


class Coordenador:

    transaction = False
    server = None
    participantes = {}
    thread = None

    def __init__(self):
        self.start_server_socket()

        # executa self.accept_connections em uma thread
        self.thread = Thread(target=self.accept_connections)
        self.thread.start()

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

            # executa self.receive(address, client) em uma thread
            thread = Thread(target=self.receive, args=(address, client))
            thread.start()

            self.participantes[address] = {
                'socket': client,
                'thread': thread,
                'can_commit': True,
            }

    def receive(self, address, participante):
        while True:
            try:
                message = participante.recv(1024).decode("utf-8")
                if not message:
                    raise ConnectionResetError

                retorno = JSONDecoder().decode(message)

                if 'can_commit' in retorno:
                    self.participantes[address]['can_commit'] = retorno['can_commit']

            except ConnectionResetError:
                if address in self.participantes:
                    del self.participantes[address]

    def send(self, address, message):
        if address in self.participantes:
            participante = self.participantes[address]['socket']

            try:
                participante.send(bytes(
                    JSONEncoder().encode(message),
                    "UTF-8"
                ))
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
        self.participantes[address]['can_commit'] = False
        self.send(address, {
            'method': 'creditar',
            'valor': valor,
        })

    def debitar(self, address, valor):
        self.participantes[address]['can_commit'] = False
        self.send(address, {
            'method': 'debitar',
            'valor': valor,
        })

    def can_commit(self, address):
        self.send(address, {'method': 'can_commit'})

    def do_abort(self, address):
        self.participantes[address]['can_commit'] = True
        self.send(address, {'method': 'do_abort'})

    def do_commit(self, address):
        self.send(address, {'method': 'do_commit'})

    def finish_transaction(self):
        self.test_transaction()

        list_can_commit = {k: v
                           for k, v in self.participantes.items()
                           if not v['can_commit']}

        [self.can_commit(k) for k, v in list_can_commit.items()]

        time.sleep(5)

        if len([v for k, v in self.participantes.items() if not v['can_commit']]):
            [self.do_abort(k) for k, v in list_can_commit.items()]
            print('Abortado')
        else:
            [self.do_commit(k) for k, v in list_can_commit.items()]
            print('Commit realizado')

        self.transaction = False


