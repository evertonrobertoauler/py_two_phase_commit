import socket
from threading import Thread
import psycopg2

from json import JSONEncoder, JSONDecoder


class Participante:

    db = None
    conn = None
    transacao = False

    def __init__(self, ip):
        self.db = psycopg2.connect("dbname=two_phase_commit user=postgres host=%s" % ip).cursor()
        self.db.execute('BEGIN')

    def connect(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((socket.gethostname(), 4000))

        self.transacao = True

        thread = Thread(target=self.receive)
        thread.start()

    def receive(self):
        while True:
            try:
                message = self.conn.recv(1024).decode("utf-8")

                if not message:
                    raise ConnectionResetError()

                msg = JSONDecoder().decode(message)

                eval("self.%s(%s)" % (msg["method"], "valor" in msg and msg["valor"] or ""))
            except Exception as e:
                self.transacao = False

    def send(self, message):
        self.conn.send(bytes(JSONEncoder().encode(message), "UTF-8"))

    def creditar(self, valor):

        self.db.execute("""
          UPDATE conta SET vl_saldo = vl_saldo + %f
        """ % valor)

    def debitar(self, valor):
        self.db.execute("""
          UPDATE conta SET vl_saldo = vl_saldo - %f
        """ % valor)

    def can_commit(self):
        self.send({'can_commit': self.transacao})

    def do_commit(self):
        self.db.execute('COMMIT')
        self.db.execute('BEGIN')
        self.transacao = True

    def do_abort(self):
        self.db.execute('ROLLBACK')
        self.db.execute('BEGIN')
        self.transacao = True

    def run(self):
        self.connect()


if __name__ == '__main__':
    try:
        Participante("172.17.0.2").run()
        Participante("172.17.0.3").run()
    except Exception as e:
        print("Erro:", e)