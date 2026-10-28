from unittest.mock import Mock

import pytest

from atribuicoes.parser_atribuicao import atribuicao


def test_parse_valido():
    parser = Mock()
    parser.expect.return_value.lexema = "x"
    parser.expressao.return_value = 10

    resultado = atribuicao(parser, lambda nome, valor: (nome, valor))

    assert resultado == ("x", 10)


def test_parse_valido_com_outra_expressao():
    parser = Mock()
    parser.expect.return_value.lexema = "total"
    parser.expressao.return_value = 20

    resultado = atribuicao(parser, lambda nome, valor: (nome, valor))

    assert resultado == ("total", 20)


def test_parse_invalido():
    parser = Mock()
    parser.expect.side_effect = SyntaxError

    with pytest.raises(SyntaxError):
        atribuicao(parser, Mock())
