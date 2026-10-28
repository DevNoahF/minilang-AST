import pytest
from unittest.mock import Mock

from atribuicoes.parser_atribuicao import atribuicao


def test_atribuicao_sem_ponto_e_virgula():
    parser = Mock()
    parser.expect.side_effect = [
        Mock(lexema="x"),
        None,
        SyntaxError()
    ]

    with pytest.raises(SyntaxError):
        atribuicao(parser, Mock())


def test_atribuicao_valida():
    parser = Mock()
    parser.expect.return_value.lexema = "idade"
    parser.expressao.return_value = 18

    resultado = atribuicao(parser, lambda nome, valor: (nome, valor))

    assert resultado == ("idade", 18)


def test_atribuicao_sem_operador_de_atribuicao():
    parser = Mock()
    parser.expect.side_effect = [Mock(lexema="idade"), SyntaxError()]

    with pytest.raises(SyntaxError):
        atribuicao(parser, Mock())
