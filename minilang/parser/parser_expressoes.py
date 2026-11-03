def expressao(parser, criar_binaria):
    esquerda = comparacao(parser, criar_binaria)
    while parser.peek().type in ("EQUAL_EQUAL", "BANG_EQUAL"):
        operador = parser.advance()
        direita = comparacao(parser, criar_binaria)
        esquerda = criar_binaria(operador.lexeme, esquerda, direita)

    return esquerda


def comparacao(parser, criar_binaria):
    esquerda = adicao(parser, criar_binaria)
    while parser.peek().type in ("LESS", "LESS_EQUAL", "GREATER", "GREATER_EQUAL"):
        operador = parser.advance()
        direita = adicao(parser, criar_binaria)
        esquerda = criar_binaria(operador.lexeme, esquerda, direita)

    return esquerda


def adicao(parser, criar_binaria):
    esquerda = parser.termo()
    while parser.peek().type in ("PLUS", "MINUS"):
        operador = parser.advance()
        direita = parser.termo()
        esquerda = criar_binaria(operador.lexeme, esquerda, direita)

    return esquerda
