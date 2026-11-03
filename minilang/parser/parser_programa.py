from ..ast_nodes import Programa
from ..diagnosticos import ExceptionSyntax


def item(parser):
    token = parser.peek()

    if token.type == "KW_INT":
        return parser.declaracao()
    if token.type == "IDENT":
        return parser.atribuicao()
    if token.type == "KW_PRINT":
        return parser.saida()
    if token.type == "LBRACE":
        return parser.bloco()
    if token.type == "KW_IF":
        return parser.condicional()
    if token.type == "KW_WHILE":
        return parser.enquanto()
    if token.type == "KW_FOR":
        return parser.para()

    raise ExceptionSyntax(
        token=token,
        expected=("KW_INT", "IDENT", "KW_PRINT", "LBRACE", "KW_IF", "KW_WHILE", "KW_FOR"),
    )


def lista_itens(parser, terminador="EOF"):
    itens = []

    while not parser.at_end() and parser.peek().type != terminador:
        itens.append(parser.item())

    return itens


def programa(parser):
    itens = parser.lista_itens()
    parser.expect("EOF")
    return Programa(itens=itens)
