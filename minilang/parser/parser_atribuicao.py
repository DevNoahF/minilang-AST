def atribuicao(parser, criar_atribuicao, com_ponto_e_virgula=True):
    identificador = parser.expect("IDENT")
    parser.expect("ASSIGN")
    expressao = parser.expressao()
    if com_ponto_e_virgula:
        parser.expect("SEMICOLON")
    no = criar_atribuicao(identificador.lexeme, expressao)
    if hasattr(no, "token"):
        no.token = identificador
    return no
