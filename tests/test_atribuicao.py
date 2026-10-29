from unittest.mock import Mock

import pytest

from minilang.parser_atribuicao import atribuicao


def test_atribuicao_sem_ponto_e_virgula():
    parser = Mock()
    parser.expect.side_effect = [
        Mock(lexeme="x"),
        None,
        SyntaxError()
    ]

    with pytest.raises(SyntaxError):
        atribuicao(parser, Mock())


def test_atribuicao_valida():
    parser = Mock()
    parser.expect.return_value.lexeme = "idade"
    parser.expressao.return_value = 18

    resultado = atribuicao(parser, lambda nome, valor: (nome, valor))

    assert resultado == ("idade", 18)


def test_atribuicao_sem_operador_de_atribuicao():
    parser = Mock()
    parser.expect.side_effect = [Mock(lexeme="idade"), SyntaxError()]

    with pytest.raises(SyntaxError):
        atribuicao(parser, Mock())

def test_expressao_invalida():
    parser = Mock()
    parser.expressao.side_effect = SyntaxError

    with pytest.raises(SyntaxError):
        atribuicao(parser, Mock())


def test_expressao_valida():
    parser = Mock()
    parser.expect.return_value.lexeme = "resultado"
    parser.expressao.return_value = 30

    resultado = atribuicao(parser, lambda nome, valor: (nome, valor))

    assert resultado == ("resultado", 30)


def test_expressao_operador_sem_valor():
    parser = Mock()
    parser.expressao.side_effect = SyntaxError("Operador sem valor")

    with pytest.raises(SyntaxError, match="Operador sem valor"):
        atribuicao(parser, Mock())

def test_parse_valido():
    parser = Mock()
    parser.expect.return_value.lexeme = "x"
    parser.expressao.return_value = 10

    resultado = atribuicao(parser, lambda nome, valor: (nome, valor))

    assert resultado == ("x", 10)


def test_parse_valido_com_outra_expressao():
    parser = Mock()
    parser.expect.return_value.lexeme = "total"
    parser.expressao.return_value = 20

    resultado = atribuicao(parser, lambda nome, valor: (nome, valor))

    assert resultado == ("total", 20)


def test_parse_invalido():
    parser = Mock()
    parser.expect.side_effect = SyntaxError

    with pytest.raises(SyntaxError):
        atribuicao(parser, Mock())
