from .ast_nodes import Atribuicao, Binaria, Declaracao, Inteiro, Saida, Variavel
from .diagnosticos import ExceptionSyntax
from .parser_atribuicao import atribuicao
from .parser_expressoes import expressao
from .parser_programa import item, lista_itens, programa


class Parser:
    def __init__(self, tokens):
        self.tokens = list(tokens)
        if not self.tokens or self.tokens[-1].type != "EOF":
            ExceptionSyntax(
                token=self.tokens[-1] if self.tokens else None,
                expected="EOF",
            )
        self.current = 0

    def peek(self):
        return self.tokens[self.current]

    def advance(self):
        token = self.peek()
        if not self.at_end():
            self.current += 1
        return token

    def expect(self, expected):
        if self.peek().type != expected:
            raise ExceptionSyntax(self.peek(), expected)
        return self.advance()

    def match(self, expected):
        if self.peek().type in expected:
            self.advance()
            return True
        return False

    def at_end(self):
        return self.peek().type == "EOF"

    def declaracao(self):
        self.expect("KW_INT")
        nome = self.expect("IDENT")
        self.expect("SEMICOLON")
        return Declaracao(nome.lexeme)

    def fator(self):
        token = self.peek()
        if token.type == "INT_LITERAL":
            self.advance()
            return Inteiro(int(token.lexeme))
        if token.type == "IDENT":
            self.advance()
            return Variavel(token.lexeme)
        if self.match("LPAREN"):
            no = self.expressao()
            self.expect("RPAREN")
            return no
        raise ExceptionSyntax(
            token, ("INT_LITERAL", "IDENT", "LPAREN")
        )

    def termo(self):
        esquerda = self.fator()
        while self.peek().type in ("STAR", "SLASH"):
            operador = self.advance()
            direita = self.fator()
            esquerda = Binaria(operador.lexeme, esquerda, direita)
        return esquerda

    def saida(self):
        self.expect("KW_PRINT")
        self.expect("LPAREN")
        no = self.expressao()
        self.expect("RPAREN")
        self.expect("SEMICOLON")
        return Saida(no)

    def expressao(self):
        return expressao(self, Binaria)

    def atribuicao(self):
        return atribuicao(self, Atribuicao)

    def item(self):
        return item(self)

    def lista_itens(self):
        return lista_itens(self)

    def programa(self):
        return programa(self)
