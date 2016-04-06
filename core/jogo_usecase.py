class RodadaEntitySpy(object):

    def __init__(self):
        self.obter_demais_jogadores_return = None
        self.obter_jogador_origem_return = None
        self.obter_todos_os_jogadores_return = None
        self.ha_proximo_jogador_destino_return = None
        self.obter_jogador_destino_return = None
        self.obter_jogador_origem_spied = False

    def obter_jogador_origem(self):
        self.obter_jogador_origem_spied = True
        return self.obter_jogador_origem_return

    def obter_demais_jogadores(self):
        return self.obter_demais_jogadores_return

    def obter_todos_os_jogadores(self):
        return self.obter_todos_os_jogadores_return

    def eliminar(self, jogador):
        pass

    def ha_proximo_jogador_destino(self):
        return self.ha_proximo_jogador_destino_return

    def obter_jogador_destino(self):
        return self.obter_jogador_destino_return

    def desabilitar(self, jogador_origem):
        pass


class JogadorGatewaySpy(object):

    def __init__(self):
        self.seu_palpite_return = None
        self.se_possui_algum_palpite_return = None
        self.informar_ao_jogador_spied = None
        self.sua_resposta_return = None
        self.se_possui_alguma_pergunta_return = None
        self.sua_pergunta_return = None
        self.informar_aos_jogadores_spied = None
        self.se_possui_alguma_resposta_return = None
        self.que_o_jogador_spied = None
        self.responde_com_spied = None
        self.possui_resposta_spied = False

    def informar_aos(self, jogadores):
        self.informar_aos_jogadores_spied = jogadores
        return self

    def o_inicio_da_rodada(self):
        pass

    def perguntar_para_o(self, jogador):

        return self

    def se_possui_alguma_pergunta(self):
        return self.se_possui_alguma_pergunta_return

    def se_possui_algum_palpite(self):
        return self.se_possui_algum_palpite_return

    def que_o(self, jogador):
        self.que_o_jogador_spied = jogador
        return self

    def pulou_a_vez(self):
        pass

    def o_fim_da_rodada(self):
        pass

    def obter_do(self, jogador):
        return self

    def sua_pergunta(self):
        return self.sua_pergunta_return

    def informar_ao(self, jogador):
        self.informar_ao_jogador_spied = jogador
        return self

    def eliminacao_por_atitude_desportiva(self):
        pass

    def foi_eliminado_por_atitude_desportiva(self):
        pass

    def as_cartas(self, cartas):
        pass

    def fez_para_o(self, jogador_destino):
        return self

    def a_pergunta(self, pergunta):
        pass

    def se_possui_alguma_resposta(self):
        return self.se_possui_alguma_resposta_return

    def nao_possui_resposta(self):
        pass

    def sua_resposta(self):
        return self.sua_resposta_return

    def responde_com(self, resposta):
        self.responde_com_spied = resposta

    def possui_resposta(self):
        self.possui_resposta_spied = True

    def seu_palpite(self):
        return self.seu_palpite_return

    def palpita_com(self, palpite):
        pass

    def que_acertou_o_palpite(self):
        pass

    def o_fim_do_jogo(self):
        pass

    def que_errou_o_palpite(self):
        pass

    def errou_o_palpite(self):
        pass


class CartaEntitySpy(object):
    def __init__(self):
        self.acertou_crime_com_o_palpite_return = None
        self.possui_todas_as_cartas_do_palpite_return = None
        self.possui_todas_as_cartas_da_pergunta_return = None

    def validar_se(self, jogador_origem):
        return self

    def possui_todas_as_cartas_da(self, pergunta):
        return self.possui_todas_as_cartas_da_pergunta_return

    def obter_cartas_do(self, jogador):
        pass

    def possui_alguma_carta(self):
        pass

    def possui_todas_as_cartas_do(self, palpite):
        return self.possui_todas_as_cartas_do_palpite_return

    def acertou_crime_com_o(self, palpite):
        return self.acertou_crime_com_o_palpite_return


class FimDoJogoException(Exception):
    pass


def manager_loop(function):

    def func_wrapper(self):
        self.loop_proxima_rodada += 1

        if self._parar_jogo():
            raise FimDoJogoException()

        function(self)

    return func_wrapper


class JogoUsecase(object):

    def __init__(self):
        self.loop_proxima_rodada = 0
        self.carta_entity = CartaEntitySpy()
        self.rodada_entity = RodadaEntitySpy()
        self.jogador_gateway = JogadorGatewaySpy()

    def executar(self):
        try:
            self._proxima_rodada()
        except FimDoJogoException:
            return

    def _proxima_rodada(self):
        jogador_origem = self.rodada_entity.obter_jogador_origem()
        demais_jogadores = self.rodada_entity.obter_demais_jogadores()
        jogadores = self.rodada_entity.obter_todos_os_jogadores()
        self.jogador_gateway.informar_aos(jogadores).o_inicio_da_rodada()

        if self.jogador_gateway.perguntar_para_o(jogador_origem).se_possui_alguma_pergunta():
            pergunta = self.jogador_gateway.obter_do(jogador_origem).sua_pergunta()

            if self.carta_entity.validar_se(jogador_origem).perguntou_com(pergunta).cartas_validas():
                self._proxima_rodada_de_respostas(jogador_origem, pergunta, demais_jogadores, jogadores)

            else:
                self._eliminar_jogador_por_atitude_desportiva(jogador_origem, jogadores)
                self._proxima_rodada()

        elif self.jogador_gateway.perguntar_para_o(jogador_origem).se_possui_algum_palpite():
            palpite = self.jogador_gateway.obter_do(jogador_origem).seu_palpite()

            if self.carta_entity.validar_se(jogador_origem).palpitou_com(palpite).cartas_validas():
                self.jogador_gateway.informar_aos(demais_jogadores).que_o(jogador_origem).palpita_com(palpite)

                if self.carta_entity.acertou_crime_com_o(palpite):
                    self.jogador_gateway.informar_aos(jogadores).que_o(jogador_origem).que_acertou_o_palpite()
                    self.jogador_gateway.informar_aos(jogadores).o_fim_do_jogo()
                    self._finalizar_jogo()

                else:
                    self.jogador_gateway.informar_ao(jogador_origem).que_errou_o_palpite()
                    self.jogador_gateway.informar_aos(jogadores).que_o(jogador_origem).errou_o_palpite()
                    self.jogador_gateway.informar_aos(jogadores).o_fim_da_rodada()
                    self.rodada_entity.desabilitar(jogador_origem)
                    self._proxima_rodada()

            else:
                self._eliminar_jogador_por_atitude_desportiva(jogador_origem, jogadores)
                self._proxima_rodada()

        else:
            self.jogador_gateway.informar_aos(demais_jogadores).que_o(jogador_origem).pulou_a_vez()
            self.jogador_gateway.informar_aos(jogadores).o_fim_da_rodada()
            self._proxima_rodada()

    def _proxima_rodada_de_respostas(self, jogador_origem, pergunta, demais_jogadores, jogadores):
        if self.rodada_entity.ha_proximo_jogador_destino():
            jogador_destino = self.rodada_entity.obter_jogador_destino()
            self.jogador_gateway.informar_aos(demais_jogadores).que_o(jogador_origem).fez_para_o(jogador_destino).a_pergunta(pergunta)

            if self.jogador_gateway.perguntar_para_o(jogador_destino).se_possui_alguma_resposta():
                resposta = self.jogador_gateway.obter_do(jogador_destino).sua_resposta()
                self.jogador_gateway.informar_ao(jogador_origem).que_o(jogador_destino).responde_com(resposta)
                self.jogador_gateway.informar_aos(demais_jogadores).que_o(jogador_destino).possui_resposta()

            else:
                if self.carta_entity.validar_se(jogador_destino).possui_alguma_carta_da(pergunta):
                    self._eliminar_jogador_por_atitude_desportiva(jogador_destino, jogadores)
                    self._proxima_rodada_de_respostas(jogador_origem, pergunta, demais_jogadores, jogadores)

                else:
                    self.jogador_gateway.informar_aos(jogadores).que_o(jogador_destino).nao_possui_resposta()
                    self._proxima_rodada_de_respostas(jogador_origem, pergunta, demais_jogadores, jogadores)

        self.jogador_gateway.informar_aos(jogadores).o_fim_da_rodada()
        self._proxima_rodada()

    def _eliminar_jogador_por_atitude_desportiva(self, jogador, jogadores):
        self.jogador_gateway.informar_ao(jogador).eliminacao_por_atitude_desportiva()
        self.jogador_gateway.informar_aos(jogadores).que_o(jogador).foi_eliminado_por_atitude_desportiva()
        self.jogador_gateway.informar_aos(jogadores).as_cartas(self.carta_entity.obter_cartas_do(jogador))
        self.rodada_entity.eliminar(jogador)

    def _finalizar_jogo(self):
        raise FimDoJogoException()

    def _parar_jogo(self):
        return False
