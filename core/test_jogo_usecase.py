from unittest import TestCase
from core.jogo_usecase import JogoUsecase, FimDoJogoException


class Jogador(object):

    def __init__(self, jogador_id):
        self.jogador_id = jogador_id


MAX_LOOP = 2
COUNT_LOOP = 0


def test_decorator(function):

    def func_wrapper(*args, **kwargs):

        if function.func_globals == MAX_LOOP:
            raise FimDoJogoException()

        return function(*args, **kwargs)

    return func_wrapper


class JogoUsecaseTestCase(TestCase):

    def setUp(self):

        self.usecase = JogoUsecase()

        JogoUsecase.contador_loop = 0
        JogoUsecase._proxima_rodada = test_decorator(JogoUsecase._proxima_rodada)

        # self.usecase._proxima_rodada = test_decorator(self.usecase._proxima_rodada)(self.usecase)

        self.usecase._parar_jogo = lambda: self.usecase.loop_proxima_rodada == 2

        # jogador_1 = Jogador()
        # self.usecase.rodada_entity.obter_jogador_origem_return = jogador_1
        #
        # jogador_2 = Jogador()
        # jogador_3 = Jogador()
        # demais_jogadores = [jogador_2, jogador_3]
        # self.usecase.rodada_entity.obter_demais_jogadores_return = demais_jogadores
        #
        # todos_os_jogadores = [jogador_1, jogador_2, jogador_3]
        # self.usecase.rodada_entity.obter_todos_os_jogadores_return = todos_os_jogadores


class JogoUsecaseTests(JogoUsecaseTestCase):

    def test_obtem_jogador_origem(self):
        self.usecase.executar()

        self.assertTrue(self.usecase.rodada_entity.obter_jogador_origem_spied)


class Pergunta(object):
    pass


class Resposta(object):
    pass


class Palpite(object):
    pass


class QuandoJogadorOrigemPossuiUmaPerguntaTests(JogoUsecaseTestCase):

    def test_obtem_pergunta(self):
        jogador_origem = Jogador(jogador_id=1)
        self.usecase.rodada_entity.obter_jogador_origem_return = jogador_origem
        jogador_destino = Jogador(jogador_id=2)
        demais_jogadores = [jogador_destino]
        self.usecase.rodada_entity.obter_demais_jogadores_return = demais_jogadores
        jogadores = [jogador_origem, jogador_destino]
        self.usecase.rodada_entity.obter_demais_jogadores_return = jogadores
        self.usecase.jogador_gateway.se_possui_alguma_pergunta_return = True
        pergunta = Pergunta()
        self.usecase.jogador_gateway.sua_pergunta_return = pergunta
        self.usecase.carta_entity.possui_todas_as_cartas_da_pergunta_return = True
        self.usecase.rodada_entity.ha_proximo_jogador_destino_return = True
        self.usecase.rodada_entity.obter_jogador_destino_return = jogador_destino
        self.usecase.jogador_gateway.se_possui_alguma_resposta_return = True
        resposta = Resposta()
        self.usecase.jogador_gateway.sua_resposta_return = resposta

        self.usecase.executar()

    def test_acertou_palpite(self):
        jogador_origem = Jogador(jogador_id=1)
        self.usecase.rodada_entity.obter_jogador_origem_return = jogador_origem
        jogador_destino = Jogador(jogador_id=2)
        demais_jogadores = [jogador_destino]
        self.usecase.rodada_entity.obter_demais_jogadores_return = demais_jogadores
        jogadores = [jogador_origem, jogador_destino]
        self.usecase.rodada_entity.obter_demais_jogadores_return = jogadores
        self.usecase.jogador_gateway.se_possui_alguma_pergunta_return = False
        self.usecase.jogador_gateway.se_possui_algum_palpite_return = True
        palpite = Palpite()
        self.usecase.jogador_gateway.seu_palpite_return = palpite
        self.usecase.carta_entity.possui_todas_as_cartas_do_palpite_return = True
        self.usecase.carta_entity.acertou_crime_com_o_palpite_return = True

        self.usecase.executar()

    def test_errou_palpite(self):
        jogador_origem = Jogador(jogador_id=1)
        self.usecase.rodada_entity.obter_jogador_origem_return = jogador_origem
        jogador_destino = Jogador(jogador_id=2)
        demais_jogadores = [jogador_destino]
        self.usecase.rodada_entity.obter_demais_jogadores_return = demais_jogadores
        jogadores = [jogador_origem, jogador_destino]
        self.usecase.rodada_entity.obter_demais_jogadores_return = jogadores
        self.usecase.jogador_gateway.se_possui_alguma_pergunta_return = False
        self.usecase.jogador_gateway.se_possui_algum_palpite_return = True
        palpite = Palpite()
        self.usecase.jogador_gateway.seu_palpite_return = palpite
        self.usecase.carta_entity.possui_todas_as_cartas_do_palpite_return = True
        self.usecase.carta_entity.acertou_crime_com_o_palpite_return = False

        self.usecase.executar()

    def test_cartas_do_palpite_nao_pertencem_ao_jogador(self):
        jogador_origem = Jogador(jogador_id=1)
        self.usecase.rodada_entity.obter_jogador_origem_return = jogador_origem
        jogador_destino = Jogador(jogador_id=2)
        demais_jogadores = [jogador_destino]
        self.usecase.rodada_entity.obter_demais_jogadores_return = demais_jogadores
        jogadores = [jogador_origem, jogador_destino]
        self.usecase.rodada_entity.obter_demais_jogadores_return = jogadores
        self.usecase.jogador_gateway.se_possui_alguma_pergunta_return = False
        self.usecase.jogador_gateway.se_possui_algum_palpite_return = True
        palpite = Palpite()
        self.usecase.jogador_gateway.seu_palpite_return = palpite
        self.usecase.carta_entity.possui_todas_as_cartas_do_palpite_return = False

        self.usecase.executar()
