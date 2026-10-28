"""Reconhecimento de comandos e do programa completo (pessoa 3).

As funções recebem a instância de Parser e podem ser associadas à classe:

    from programa.parser_programa import item, lista_itens, programa

    class Parser:
        item = item
        lista_itens = lista_itens
        programa = programa

O Parser compartilhado deve fornecer peek(), at_end(), expect(tipo),
declaracao(), atribuicao() e saida(). Cada token deve ter os atributos tipo,
linha e coluna. Os métodos de comando consomem seus próprios tokens e retornam
os respectivos nós da AST.

Na integração, a base comum deve fornecer ast_nodes.Programa(itens) e exportar
ErroSintatico pelo pacote diagnostico. Esses componentes não são implementados
aqui, pois pertencem à base compartilhada e à parte de diagnósticos.
"""

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
