from ast_nodes import Programa
from diagnostico import ErroSintatico


def item(parser):
    """Seleciona o comando pelo token atual e delega seu reconhecimento."""
    token = parser.peek()

    if token.tipo == "INT":
        return parser.declaracao()
    if token.tipo == "ID":
        return parser.atribuicao()
    if token.tipo == "PRINT":
        return parser.saida()

    raise ErroSintatico(
        token_encontrado=token,
        tipos_esperados=("INT", "ID", "PRINT"),
        linha=token.linha,
        coluna=token.coluna,
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
