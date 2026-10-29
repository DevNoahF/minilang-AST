from .ast_nodes import Programa
from .diagnosticos import ExceptionSyntax


def item(parser):
    """Seleciona o comando pelo token atual e delega seu reconhecimento."""
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
    """Retorna os comandos na ordem de leitura, deixando EOF para programa()."""
    itens = []

    while not parser.at_end():
        itens.append(parser.item())

    return itens


def programa(parser):
    """Reconhece zero ou mais comandos, exige EOF e retorna a raiz da AST."""
    itens = parser.lista_itens()
    parser.expect("EOF")
    return Programa(itens=itens)
