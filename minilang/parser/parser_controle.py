from ..ast_nodes import Bloco, Condicional, Enquanto, Para


def bloco(parser):
    parser.expect("LBRACE")
    itens = parser.lista_itens("RBRACE")
    parser.expect("RBRACE")
    return Bloco(itens)


def condicional(parser):
    parser.expect("KW_IF")
    parser.expect("LPAREN")
    condicao = parser.expressao()
    parser.expect("RPAREN")
    entao = parser.bloco()
    return Condicional(condicao, entao)


def enquanto(parser):
    parser.expect("KW_WHILE")
    parser.expect("LPAREN")
    condicao = parser.expressao()
    parser.expect("RPAREN")
    corpo = parser.bloco()
    return Enquanto(condicao, corpo)


def para(parser):
    parser.expect("KW_FOR")
    parser.expect("LPAREN")

    inicializacao = None
    if parser.peek().type == "KW_INT":
        inicializacao = parser.declaracao()
    elif parser.peek().type == "SEMICOLON":
        parser.advance()
    else:
        inicializacao = parser.atribuicao()

    condicao = None
    if parser.peek().type != "SEMICOLON":
        condicao = parser.expressao()
    parser.expect("SEMICOLON")

    atualizacao = None
    if parser.peek().type != "RPAREN":
        atualizacao = parser.atribuicao(com_ponto_e_virgula=False)
    parser.expect("RPAREN")

    corpo = parser.bloco()
    return Para(inicializacao, condicao, atualizacao, corpo)
