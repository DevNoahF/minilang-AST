from .ast_nodes import Programa
from .diagnosticos import ExceptionSyntax


def item(parser):
    token = parser.peek()

    if token.type == "KW_INT":
        return parser.declaracao()
    if token.type == "IDENT":
        return parser.atribuicao()
    if token.type == "KW_PRINT":
        return parser.saida()

    raise ExceptionSyntax(
        token=token,
        expected=("KW_INT", "IDENT", "KW_PRINT"),
    )


def lista_itens(parser):
    itens = []

    while not parser.at_end():
        itens.append(parser.item())

    return itens


def programa(parser):
    itens = parser.lista_itens()
    parser.expect("EOF")
    return Programa(itens=itens)
