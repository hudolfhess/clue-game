class Jogo(object):

    def __init__(self):
        self.gerenciador_da_rodada = None
        self.gerenciador_de_jogadores = None
        self.gerenciador_de_perguntas_e_respostas = None
        self.gerenciador_de_cartas = None

    def iniciar(self):
        self.ciclo_de_pergunta()

    def ciclo_de_pergunta(self):
        jogador_da_vez = self.gerenciador_da_rodada.obter_jogador_da_vez()

        acao = self.gerenciador_de_jogadores.solicitar_acao_ao(jogador_da_vez)

        if acao.palpite:
            self.ciclo_de_palpite(acao.palpite)

        else:
            self.ciclo_de_resposta()

    def ciclo_de_resposta(self):
        jogador_a_responder = self.gerenciador_da_rodada.obter_jogador_a_responder()

        if jogador_a_responder:
            resposta = self.gerenciador_de_jogadores.solicitar_resposta_ao(jogador_a_responder)

            if not self.gerenciador_de_cartas.existe(resposta):
                self.ciclo_de_resposta()

        self.ciclo_de_pergunta()

    def ciclo_de_palpite(self, palpite):
        if self.gerenciador_de_cartas.acertou_palpite(palpite):
            self.terminar()

        else:
            self.gerenciador_da_rodada.eliminar(palpite.jogador)
            self.gerenciador_de_jogadores.eliminar(palpite.jogador)
            self.ciclo_de_pergunta()

    def terminar(self):
        pass


class GerenciadorDePerguntasERespostas(object):

    def receber_pergunta_do_jogador(self, jogador):
        solicitar_pergunta_do_jogador(jogador)
        aguardar_pergunta_do_jogador()
        pergunta = receber_pergunta_do_jogador()
        informar_todos_os_jogadores_da_pergunta(pergunta)
        return pergunta

    def jogador_a_palpitar(self, pergunta):
        informa_todos_os_jogadores_do_palpite_feito(pergunta)
