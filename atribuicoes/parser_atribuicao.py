def atribuicao(parser, criar_atribuicao):
    identificador = parser.expect("ID")
    parser.expect("ASSIGN")
    expressao = parser.expressao()
    parser.expect("SEMICOLON")
    return criar_atribuicao(identificador.lexema, expressao)
