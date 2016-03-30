from unittest import TestCase
from core.entities.pergunta_entity import PerguntaEntity
from core.jogo import Jogo
from core.entities.jogador_entity import JogadorEntity


class GerenciarJogadoresSpy(object):

    def __init__(self):
        self.proximo_jogador_a_perguntar_return = None
        self.proximo_jogador_a_responder_return = None

    def proximo_jogador_a_perguntar(self):
        return self.proximo_jogador_a_perguntar_return

    def proximo_jogador_a_responder(self):
        return self.proximo_jogador_a_responder_return


class GerenciadorDePerguntasSpy(object):

    def __init__(self):
        self.receber_pergunta_return = None

    def jogador_a_perguntar(self, jogador_a_perguntar):
        self.jogador_a_perguntar_spied = jogador_a_perguntar

    def receber_pergunta(self):
        return self.receber_pergunta_return


class GerenciadorDeRespostasSpy(object):

    def __init__(self):
        self.receber_resposta_return = None

    def jogador_a_responder(self, jogador_a_responder):
        self.jogador_a_responder_spied = jogador_a_responder

    def resposta_do_jogador(self, resposta_do_jogador):
        self.resposta_do_jogador_spied = resposta_do_jogador

    def receber_resposta(self):
        return self.receber_resposta_return


class DelegateGatewaySpy(object):

    def __init__(self):
        self.jogador_a_perguntar_spied = None
        self.aguardar_pergunta_spied = False
        self.receber_pergunta_return = None
        self.pergunta_do_jogador_spied = None
        self.jogador_a_responder_spied = None
        self.aguardar_resposta_spied = False
        self.receber_resposta_return = None
        self.resposta_do_jogador_spied = None

    def jogador_a_perguntar(self, jogador_a_perguntar):
        self.jogador_a_perguntar_spied = jogador_a_perguntar

    def aguardar_pergunta(self):
        self.aguardar_pergunta_spied = True

    def receber_pergunta(self):
        return self.receber_pergunta_return

    def pergunta_do_jogador(self, pergunta_do_jogador):
        self.pergunta_do_jogador_spied = pergunta_do_jogador

    def jogador_a_responder(self, jogador_a_responder):
        self.jogador_a_responder_spied = jogador_a_responder

    def aguardar_resposta(self):
        self.aguardar_resposta_spied = True

    def receber_resposta(self):
        return self.receber_resposta_return

    def resposta_do_jogador(self, resposta_do_jogador):
        self.resposta_do_jogador_spied = resposta_do_jogador


class JogoTestCase(TestCase):

    def setUp(self):
        self.jogo = Jogo()
        self.jogo.gerenciador_de_jogadores = GerenciarJogadoresSpy()
        self.jogo.gerenciador_de_perguntas_e_respostas = GerenciadorDePerguntasSpy()
        self.jogo.gerenciador_de_respostas = GerenciadorDeRespostasSpy()


class JogoTests(JogoTestCase):

    def test_jogador_a_perguntar(self):
        jogador_esperado = JogadorEntity(jogador_id=1)
        self.jogo.gerenciador_de_jogadores.proximo_jogador_a_perguntar_return = jogador_esperado

        self.jogo.iniciar()

        self.assertEqual(jogador_esperado.jogador_id, self.jogo.gerenciador_de_perguntas_e_respostas.jogador_a_perguntar_spied.jogador_id)


class QuandoForPerguntaTests(JogoTestCase):

    def setUp(self):
        super(QuandoForPerguntaTests, self).setUp()

        jogador_a_perguntar = JogadorEntity(jogador_id=1)
        pergunta_esperada = PerguntaEntity(jogador_a_perguntar)
        self.jogo.gerenciador_de_perguntas_e_respostas.receber_pergunta_return = pergunta_esperada

    def test_jogador_a_responder(self):
        jogador_a_responder = JogadorEntity(jogador_id=2)
        self.jogo.gerenciador_de_jogadores.proximo_jogador_a_responder_return = jogador_a_responder

        self.jogo.iniciar()

        self.assertEqual(jogador_a_responder.jogador_id, self.jogo.gerenciador_de_respostas.jogador_a_responder_spied.jogador_id)


class QuandoForPalpiteTests(JogoTestCase):
    pass


class QuandoHouverRespostaTests(JogoTestCase):

    def setUp(self):
        super(QuandoHouverRespostaTests, self).setUp()

        jogador_a_responder = JogadorEntity(jogador_id=2)
        resposta_esperada = PerguntaEntity(jogador_a_responder)
        self.jogo.delegate_gateway.receber_resposta_return = resposta_esperada


class QuandoNaoHouverRespostaTests(JogoTestCase):
    pass
