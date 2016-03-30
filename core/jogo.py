class Jogo(object):

    def __init__(self):
        self.gerenciador_de_jogadores = None
        self.gerenciador_de_perguntas = None
        self.gerenciador_de_respostas = None

    def iniciar(self):
        jogador_a_perguntar = self.gerenciador_de_jogadores.proximo_jogador_a_perguntar()
        self.gerenciador_de_perguntas.jogador_a_perguntar(jogador_a_perguntar)

        pergunta_do_jogador = self.gerenciador_de_perguntas.receber_pergunta()

        if True:
            jogador_a_responder = self.gerenciador_de_jogadores.proximo_jogador_a_responder()
            self.gerenciador_de_respostas.jogador_a_responder(jogador_a_responder)

            resposta_do_jogador = self.gerenciador_de_respostas.receber_resposta()
        else:
            pass
