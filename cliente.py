from coordenador import Coordenador
import os
import signal


class Cliente():

    num = None
    valor = None
    coordenador = Coordenador()
    participante = None

    def __init__(self):
        self.participantes = []
        self.list_menu = [
            ["Sair", self.sair],
            ["Inicia Transação", self.inicia_transacao],
            ["Listar Participantes", self.listar_participantes],
            ["Lançar Crédito", self.lancar_credito],
            ["Lançar Débito", self.lancar_debito],
            ["Finalizar Transação", self.finalizar_transacao],
        ]

    def menu(self):
        print(" ")
        print("Menu:")
        [print(k, ":", v[0]) for k, v in enumerate(self.list_menu)]
        print("Escolha uma Opção:")

    def opcao(self):
        try:
            self.num = int(input())
            self.list_menu.__getitem__(self.num)
        except (ValueError, IndexError):
            raise Exception("Opção inválida!")

    def escolha_participante(self):
        print("Escolha um participante:")

        self.listar_participantes()

        try:
            self.participante = self.participantes[int(input())]
        except (ValueError, IndexError):
            raise Exception("Participante invalido!")

    def entrada_valor(self):
        try:
            print("Digite um valor:")
            self.valor = float(input())
        except (ValueError, IndexError):
            raise Exception("Valor inválido!")

    def sair(self):
        self.coordenador.stop()
        raise StopIteration()

    def inicia_transacao(self):
        self.coordenador.begin_transaction()
        print("Transação iniciada")

    def listar_participantes(self):

        if not len(self.coordenador.participantes):
            raise Exception("Nenhum participante encontrado!")

        print("Participantes:", len(self.coordenador.participantes))
        self.participantes = list(self.coordenador.participantes.keys())
        [print(" ", k, ":", v) for k, v in enumerate(self.participantes)]

    def lancar_credito(self):
        self.escolha_participante()
        self.entrada_valor()
        self.coordenador.creditar(self.participante, self.valor)

    def lancar_debito(self):
        self.escolha_participante()
        self.entrada_valor()
        self.coordenador.debitar(self.participante, self.valor)

    def finalizar_transacao(self):
        self.coordenador.finish_transaction()
        print("Transação finalizada")

    def run(self):
        while True:
            try:
                self.menu()
                self.opcao()
                self.list_menu[self.num][1]()
            except StopIteration:
                print("Cliente finalizado")
                os.kill(os.getsid(), signal.SIGTERM)
            except Exception as e:
                print("Erro:", e)

if __name__ == '__main__':
    Cliente().run()