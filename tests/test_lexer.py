import os
import sys
import unittest


sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from minilang.lexer import Lexer, TokenType



def tipos(source):
    tokens, _ = Lexer(source).scan_tokens()
    return [token.type for token in tokens]


def tipos_e_lexemas(source):
    tokens, _ = Lexer(source).scan_tokens()
    return [(token.type, token.lexeme) for token in tokens]


class TestLexer(unittest.TestCase):
    def test_palavras_e_identificadores(self):
        resultado = tipos_e_lexemas("int intx ifx while")
        esperado = [
            (TokenType.KW_INT, "int"),
            (TokenType.IDENT, "intx"),
            (TokenType.IDENT, "ifx"),
            (TokenType.KW_WHILE, "while"),
            (TokenType.EOF, ""),
        ]
        self.assertEqual(resultado, esperado)

    def test_numeros_e_sinais(self):
        resultado = tipos_e_lexemas("007 -10 +7")
        esperado = [
            (TokenType.INT_LITERAL, "007"),
            (TokenType.MINUS, "-"),
            (TokenType.INT_LITERAL, "10"),
            (TokenType.PLUS, "+"),
            (TokenType.INT_LITERAL, "7"),
            (TokenType.EOF, ""),
        ]
        self.assertEqual(resultado, esperado)

    def test_numero_seguido_de_nome(self):
        resultado = tipos_e_lexemas("2total total-2")
        esperado = [
            (TokenType.INT_LITERAL, "2"),
            (TokenType.IDENT, "total"),
            (TokenType.IDENT, "total"),
            (TokenType.MINUS, "-"),
            (TokenType.INT_LITERAL, "2"),
            (TokenType.EOF, ""),
        ]
        self.assertEqual(resultado, esperado)

    def test_iguais(self):
        resultado = tipos("= == ===")
        esperado = [
            TokenType.ASSIGN,
            TokenType.EQUAL_EQUAL,
            TokenType.EQUAL_EQUAL,
            TokenType.ASSIGN,
            TokenType.EOF,
        ]
        self.assertEqual(resultado, esperado)

    def test_exclamacao(self):
        tokens, erros = Lexer("!= ! <==").scan_tokens()
        esperado = [
            TokenType.BANG_EQUAL,
            TokenType.LESS_EQUAL,
            TokenType.ASSIGN,
            TokenType.EOF,
        ]
        self.assertEqual([token.type for token in tokens], esperado)
        self.assertEqual(len(erros), 1)
        self.assertEqual(erros[0].character, "!")

    def test_divisao(self):
        resultado = tipos_e_lexemas("a/b")
        esperado = [
            (TokenType.IDENT, "a"),
            (TokenType.SLASH, "/"),
            (TokenType.IDENT, "b"),
            (TokenType.EOF, ""),
        ]
        self.assertEqual(resultado, esperado)

    def test_comentario_vazio(self):
        self.assertEqual(tipos("//"), [TokenType.EOF])

    def test_comentario_com_barra(self):
        self.assertEqual(tipos("///x"), [TokenType.EOF])

    def test_delimitadores(self):
        resultado = tipos("{print(x);}")
        esperado = [
            TokenType.LBRACE,
            TokenType.KW_PRINT,
            TokenType.LPAREN,
            TokenType.IDENT,
            TokenType.RPAREN,
            TokenType.SEMICOLON,
            TokenType.RBRACE,
            TokenType.EOF,
        ]
        self.assertEqual(resultado, esperado)

    def test_entrada_vazia(self):
        tokens, erros = Lexer("").scan_tokens()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.EOF)
        self.assertEqual((tokens[0].line, tokens[0].column), (1, 1))
        self.assertEqual(erros, [])

    def test_caractere_invalido(self):
        tokens, erros = Lexer("@x").scan_tokens()
        self.assertEqual(len(erros), 1)
        self.assertEqual(erros[0].character, "@")
        self.assertEqual((erros[0].line, erros[0].column), (1, 1))
        self.assertEqual(tokens[0].type, TokenType.IDENT)
        self.assertEqual(tokens[0].lexeme, "x")
        self.assertEqual((tokens[0].line, tokens[0].column), (1, 2))
        self.assertEqual((tokens[1].line, tokens[1].column), (1, 3))

    def test_tab(self):
        tokens, _ = Lexer("\tprint").scan_tokens()
        self.assertEqual(tokens[0].type, TokenType.KW_PRINT)
        self.assertEqual((tokens[0].line, tokens[0].column), (1, 2))
        self.assertEqual((tokens[1].line, tokens[1].column), (1, 7))

    def test_dois_erros(self):
        tokens, erros = Lexer("! @ !=").scan_tokens()
        self.assertEqual(len(erros), 2)
        self.assertEqual(erros[0].character, "!")
        self.assertEqual((erros[0].line, erros[0].column), (1, 1))
        self.assertEqual(erros[1].character, "@")
        self.assertEqual((erros[1].line, erros[1].column), (1, 3))
        self.assertEqual(tokens[0].type, TokenType.BANG_EQUAL)
        self.assertEqual((tokens[0].line, tokens[0].column), (1, 5))
        self.assertEqual((tokens[1].line, tokens[1].column), (1, 7))

    def test_letra_com_acento(self):
        tokens, erros = Lexer("vãlor").scan_tokens()
        self.assertEqual(len(erros), 1)
        self.assertEqual(erros[0].character, "ã")
        self.assertEqual((erros[0].line, erros[0].column), (1, 2))
        self.assertEqual((tokens[0].type, tokens[0].lexeme), (TokenType.IDENT, "v"))
        self.assertEqual((tokens[1].type, tokens[1].lexeme), (TokenType.IDENT, "lor"))
        self.assertEqual((tokens[2].line, tokens[2].column), (1, 6))


    def test_if_com_comparacao(self):
        resultado = tipos("if(total2>=10){print(total2);}")
        esperado = [
            TokenType.KW_IF,
            TokenType.LPAREN,
            TokenType.IDENT,
            TokenType.GREATER_EQUAL,
            TokenType.INT_LITERAL,
            TokenType.RPAREN,
            TokenType.LBRACE,
            TokenType.KW_PRINT,
            TokenType.LPAREN,
            TokenType.IDENT,
            TokenType.RPAREN,
            TokenType.SEMICOLON,
            TokenType.RBRACE,
            TokenType.EOF,
        ]
        self.assertEqual(resultado, esperado)

    def test_intx(self):
        resultado = tipos_e_lexemas("intx===007;")
        esperado = [
            (TokenType.IDENT, "intx"),
            (TokenType.EQUAL_EQUAL, "=="),
            (TokenType.ASSIGN, "="),
            (TokenType.INT_LITERAL, "007"),
            (TokenType.SEMICOLON, ";"),
            (TokenType.EOF, ""),
        ]
        self.assertEqual(resultado, esperado)

    def test_while1(self):
        resultado = tipos_e_lexemas("while1 != while")
        esperado = [
            (TokenType.IDENT, "while1"),
            (TokenType.BANG_EQUAL, "!="),
            (TokenType.KW_WHILE, "while"),
            (TokenType.EOF, ""),
        ]
        self.assertEqual(resultado, esperado)

    def test_numero_e_if(self):
        resultado = tipos_e_lexemas("2if <= 03")
        esperado = [
            (TokenType.INT_LITERAL, "2"),
            (TokenType.KW_IF, "if"),
            (TokenType.LESS_EQUAL, "<="),
            (TokenType.INT_LITERAL, "03"),
            (TokenType.EOF, ""),
        ]
        self.assertEqual(resultado, esperado)

    def test_tres_iguais(self):
        tokens, erros = Lexer("===").scan_tokens()
        resultado = [(token.type, token.lexeme) for token in tokens]
        esperado = [
            (TokenType.EQUAL_EQUAL, "=="),
            (TokenType.ASSIGN, "="),
            (TokenType.EOF, ""),
        ]
        self.assertEqual(resultado, esperado)
        self.assertEqual(erros, [])


    def test_varios_invalidos(self):
        tokens, erros = Lexer("@@@@@").scan_tokens()
        self.assertEqual(len(erros), 5)
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.EOF)

    def test_posicao_do_eof(self):
        tokens, _ = Lexer("x").scan_tokens()
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[-1].type, TokenType.EOF)
        self.assertEqual((tokens[-1].line, tokens[-1].column), (1, 2))


if __name__ == "__main__":
    unittest.main()
