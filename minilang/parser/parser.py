from ..ast_nodes import Atribuicao, Binaria, Booleano, Declaracao, Inteiro, Saida, Variavel
from ..diagnosticos import ExceptionSyntax
from .parser_atribuicao import atribuicao
from .parser_controle import bloco, condicional, enquanto, para
from .parser_expressoes import expressao
from .parser_programa import item, lista_itens, programa


class Parser:
    def __init__(self, tokens):
        self.tokens = list(tokens)
        if not self.tokens or self.tokens[-1].type != "EOF":
            raise ValueError("A lista de tokens deve terminar com EOF")
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

    def match(self, *expected):
        if self.peek().type in expected:
            self.advance()
            return True
        return False

    def at_end(self):
        return self.peek().type == "EOF"

    def declaracao(self):
        tipo = self.advance()
        if tipo.type not in ("KW_INT", "KW_BOOL"):
            raise ExceptionSyntax(tipo, ("KW_INT", "KW_BOOL"))
        nome = self.expect("IDENT")
        inicializador = None
        if self.match("ASSIGN"):
            inicializador = self.expressao()
        self.expect("SEMICOLON")
        return Declaracao(nome.lexeme, inicializador, tipo.lexeme, nome)

    def fator(self):
        token = self.peek()
        if token.type == "INT_LITERAL":
            self.advance()
            return Inteiro(int(token.lexeme), token)
        if token.type in ("KW_TRUE", "KW_FALSE"):
            self.advance()
            return Booleano(token.type == "KW_TRUE", token)
        if token.type == "IDENT":
            self.advance()
            return Variavel(token.lexeme, token)
        if self.match("LPAREN"):
            no = self.expressao()
            self.expect("RPAREN")
            return no
        raise ExceptionSyntax(
            token, ("INT_LITERAL", "IDENT", "LPAREN", "KW_TRUE", "KW_FALSE")
        )

    def termo(self):
        esquerda = self.fator()
        while self.peek().type in ("STAR", "SLASH"):
            operador = self.advance()
            direita = self.fator()
            esquerda = Binaria(operador.lexeme, esquerda, direita, operador)
        return esquerda

    def saida(self):
        self.expect("KW_PRINT")
        self.expect("LPAREN")
        no = self.expressao()
        self.expect("RPAREN")
        self.expect("SEMICOLON")
        return Saida(no)

    def expressao(self):
        return expressao(self, self.criar_binaria)

    def criar_binaria(self, operador, esquerda, direita):
        return Binaria(operador.lexeme, esquerda, direita, operador)

    def atribuicao(self, com_ponto_e_virgula=True):
        return atribuicao(self, Atribuicao, com_ponto_e_virgula)

    def bloco(self):
        return bloco(self)

    def condicional(self):
        return condicional(self)

    def enquanto(self):
        return enquanto(self)

    def para(self):
        return para(self)

    def item(self):
        return item(self)

    def lista_itens(self, terminador="EOF"):
        return lista_itens(self, terminador)

    def programa(self):
        return programa(self)
