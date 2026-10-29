def expressao(parser, criar_binaria):
    """Reconhece somas e subtracoes, agrupando a AST a esquerda."""
    esquerda = parser.termo()

    while parser.peek().type in ("PLUS", "MINUS"):
        operador = parser.advance()
        direita = parser.termo()
        esquerda = criar_binaria(operador.lexeme, esquerda, direita)

    return esquerda
