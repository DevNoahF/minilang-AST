import pytest
from unittest.mock import Mock

from atribuicoes.parser_atribuicao import atribuicao


def test_expressao_invalida():
    parser = Mock()
    parser.expressao.side_effect = SyntaxError

    with pytest.raises(SyntaxError):
        atribuicao(parser, Mock())


def test_expressao_valida():
    parser = Mock()
    parser.expect.return_value.lexema = "resultado"
    parser.expressao.return_value = 30

    resultado = atribuicao(parser, lambda nome, valor: (nome, valor))

    assert resultado == ("resultado", 30)


def test_expressao_operador_sem_valor():
    parser = Mock()
    parser.expressao.side_effect = SyntaxError("Operador sem valor")

    with pytest.raises(SyntaxError, match="Operador sem valor"):
        atribuicao(parser, Mock())
