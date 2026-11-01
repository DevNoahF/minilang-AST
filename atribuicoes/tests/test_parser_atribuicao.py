import unittest
from collections import deque
from unittest.mock import Mock, call

from minilang.parser.parser_atribuicao import atribuicao


class TestAtribuicao(unittest.TestCase):
    def setUp(self):
        self.parser = Mock()
        self.parser.expect.return_value = Mock(lexeme="x")
        self.parser.expressao.return_value = {"valor": 10}

        def criar_no(nome, expressao):
            return (nome, expressao)

        self.criar_atribuicao = Mock(side_effect=criar_no)

    def test_atribuicao_simples(self):
        resultado = atribuicao(self.parser, self.criar_atribuicao)

        self.assertEqual(resultado, ("x", {"valor": 10}))
        self.criar_atribuicao.assert_called_once_with("x", {"valor": 10})
        self.assertEqual(
            self.parser.mock_calls,
            [
                call.expect("IDENT"),
                call.expect("ASSIGN"),
                call.expressao(),
                call.expect("SEMICOLON"),
            ],
        )

    def test_expressao_composta(self):
        expressao = {"operador": "+", "esquerda": {"valor": 20}, "direita": {"valor": 5}}
        self.parser.expect.return_value.lexeme = "idade"
        self.parser.expressao.return_value = expressao

        resultado = atribuicao(self.parser, self.criar_atribuicao)

        self.assertEqual(resultado[0], "idade")
        self.assertIs(resultado[1], expressao)
        self.parser.expressao.assert_called_once_with()
        self.criar_atribuicao.assert_called_once_with("idade", expressao)

    def test_falta_identificador(self):
        erro = SyntaxError("Esperado IDENT")
        self.parser.expect.side_effect = erro

        with self.assertRaises(SyntaxError) as contexto:
            atribuicao(self.parser, self.criar_atribuicao)

        self.assertIs(contexto.exception, erro)
        self.assertEqual(self.parser.mock_calls, [call.expect("IDENT")])
        self.criar_atribuicao.assert_not_called()

    def test_falta_igual(self):
        erro = SyntaxError("Esperado ASSIGN")
        self.parser.expect.side_effect = [Mock(lexeme="x"), erro]

        with self.assertRaises(SyntaxError) as contexto:
            atribuicao(self.parser, self.criar_atribuicao)

        self.assertIs(contexto.exception, erro)
        self.assertEqual(
            self.parser.mock_calls, [call.expect("IDENT"), call.expect("ASSIGN")]
        )
        self.criar_atribuicao.assert_not_called()

    def test_expressao_invalida(self):
        erro = SyntaxError("Expressao invalida")
        self.parser.expressao.side_effect = erro

        with self.assertRaises(SyntaxError) as contexto:
            atribuicao(self.parser, self.criar_atribuicao)

        self.assertIs(contexto.exception, erro)
        self.assertEqual(
            self.parser.mock_calls,
            [call.expect("IDENT"), call.expect("ASSIGN"), call.expressao()],
        )
        self.criar_atribuicao.assert_not_called()

    def test_falta_ponto_e_virgula(self):
        erro = SyntaxError("Esperado SEMICOLON")
        self.parser.expect.side_effect = [Mock(lexeme="x"), None, erro]

        with self.assertRaises(SyntaxError) as contexto:
            atribuicao(self.parser, self.criar_atribuicao)

        self.assertIs(contexto.exception, erro)
        self.assertEqual(
            self.parser.mock_calls,
            [
                call.expect("IDENT"),
                call.expect("ASSIGN"),
                call.expressao(),
                call.expect("SEMICOLON"),
            ],
        )
        self.criar_atribuicao.assert_not_called()

    def test_preserva_proximo_comando(self):
        self.verificar_token_restante("KW_PRINT")

    def test_preserva_eof(self):
        self.verificar_token_restante("EOF")

    def verificar_token_restante(self, proximo_tipo):
        proximo_token = Mock(type=proximo_tipo)
        tokens = deque(
            [
                Mock(type="IDENT", lexeme="x"),
                Mock(type="ASSIGN"),
                Mock(type="INT_LITERAL", lexeme="10"),
                Mock(type="SEMICOLON"),
                proximo_token,
            ]
        )

        def expect(tipo):
            self.assertEqual(tokens[0].type, tipo)
            return tokens.popleft()

        def expressao():
            expect("INT_LITERAL")
            return {"valor": 10}

        self.parser.expect.side_effect = expect
        self.parser.expressao.side_effect = expressao

        resultado = atribuicao(self.parser, self.criar_atribuicao)

        self.assertEqual(resultado, ("x", {"valor": 10}))
        self.assertEqual(len(tokens), 1)
        self.assertIs(tokens[0], proximo_token)
        self.criar_atribuicao.assert_called_once_with("x", {"valor": 10})


if __name__ == "__main__":
    unittest.main()
