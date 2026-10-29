def atribuicao(parser, criar_atribuicao):
    identificador = parser.expect("IDENT")
    parser.expect("ASSIGN")
    expressao = parser.expressao()
    parser.expect("SEMICOLON")
    return criar_atribuicao(identificador.lexeme, expressao)
