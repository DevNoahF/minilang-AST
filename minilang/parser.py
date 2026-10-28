from .ast_nodes import Binaria, Declaracao, Inteiro, Saida, Variavel
from .lexer import TokenType
from .parser_atribuicao import atribuicao as _atribuicao
from .parser_expressoes import expressao as _expressao
from .parser_programa import item as _item
from .parser_programa import lista_itens as _lista_itens
from .parser_programa import programa as _programa


class ErroSintatico(Exception):
    def __init__(self, token, tipos_esperados):
        self.token_encontrado = token
        self.tipos_esperados = tuple(tipos_esperados)
        self.linha = token.line
        self.coluna = token.column

        encontrado = token.lexeme if token.lexeme else token.type
        esperado = ", ".join(self.tipos_esperados)
        super().__init__(
            f"Token inesperado {encontrado!r} ({token.type}) "
            f"na posição {self.linha}:{self.coluna}; esperado: {esperado}"
        )


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def peek(self):
        return self.tokens[self.current]

    def advance(self):
        token = self.peek()
        if token.type != TokenType.EOF:
            self.current += 1
        return token

    def at_end(self):
        return self.peek().type == TokenType.EOF

    def match(self, *tipos):
        if self.peek().type in tipos:
            self.advance()
            return True
        return False

    def expect(self, tipo):
        if self.peek().type == tipo:
            return self.advance()
        raise ErroSintatico(self.peek(), (tipo,))

    def declaracao(self):
        self.expect(TokenType.KW_INT)
        nome = self.expect(TokenType.IDENT)
        self.expect(TokenType.SEMICOLON)
        return Declaracao(nome.lexeme)

    def fator(self):
        if self.match(TokenType.INT_LITERAL):
            return Inteiro(int(self.tokens[self.current - 1].lexeme))
        if self.match(TokenType.IDENT):
            return Variavel(self.tokens[self.current - 1].lexeme)
        if self.match(TokenType.LPAREN):
            expressao = self.expressao()
            self.expect(TokenType.RPAREN)
            return expressao
        raise ErroSintatico(
            self.peek(),
            (TokenType.INT_LITERAL, TokenType.IDENT, TokenType.LPAREN),
        )

    def termo(self):
        no = self.fator()
        while self.peek().type in (TokenType.STAR, TokenType.SLASH):
            operador = self.advance()
            direita = self.fator()
            no = Binaria(no, operador.lexeme, direita)
        return no

    def saida(self):
        self.expect(TokenType.KW_PRINT)
        self.expect(TokenType.LPAREN)
        expressao = self.expressao()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)
        return Saida(expressao)

    def expressao(self):
        return _expressao(self)

    def atribuicao(self):
        return _atribuicao(self)

    def item(self):
        return _item(self)

    def lista_itens(self):
        return _lista_itens(self)

    def programa(self):
        return _programa(self)
