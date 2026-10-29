import pytest

from minilang import Lexer, Parser, Token
from minilang.ast_nodes import (
    Atribuicao, Binaria, Declaracao, Inteiro, Programa, Saida, Variavel,
)
from minilang.diagnosticos import ExceptionSyntax
from main import main, run


def tokens(*pares):
    """Dados de teste no formato do lexer antigo; nao faz analise lexica."""
    resultado = []
    coluna = 1
    for tipo, lexema in pares:
        resultado.append(Token(tipo, lexema, 1, coluna))
        coluna += len(lexema)
    resultado.append(Token("EOF", "", 1, coluna))
    return resultado


def test_peek_nao_consume_e_advance_retorna_o_token():
    entrada = tokens(("KW_INT", "int"), ("IDENT", "x"), ("SEMICOLON", ";"))
    parser = Parser(entrada)
    assert parser.peek() is entrada[0]
    assert parser.peek() is entrada[0]
    assert parser.current == 0
    assert parser.advance() is entrada[0]
    assert parser.peek() is entrada[1]


def test_expect_consume_somente_o_tipo_exigido():
    entrada = tokens(("IDENT", "x"), ("SEMICOLON", ";"))
    parser = Parser(entrada)
    assert parser.expect("IDENT") is entrada[0]
    assert parser.peek() is entrada[1]


def test_expect_preserva_token_e_informa_posicao_no_erro():
    entrada = tokens(("IDENT", "x"))
    entrada[0].line, entrada[0].column = 2, 3
    parser = Parser(entrada)
    with pytest.raises(ExceptionSyntax) as resultado:
        parser.expect("INT_LITERAL")
    erro = resultado.value
    assert erro.token is entrada[0]
    assert erro.expected == ("INT_LITERAL",)
    assert (erro.line, erro.column) == (2, 3)
    assert "IDENT ('x')" in str(erro)
    assert "INT_LITERAL" in str(erro)
    assert parser.current == 0


def test_match_so_consume_quando_corresponde():
    parser = Parser(tokens(("PLUS", "+"), ("INT_LITERAL", "2")))
    assert parser.match("MINUS") is False
    assert parser.current == 0
    assert parser.match("PLUS", "MINUS") is True
    assert parser.current == 1
    assert parser.peek().type == "INT_LITERAL"


def test_at_end_e_operacoes_no_eof():
    parser = Parser(tokens(("IDENT", "x")))
    assert parser.at_end() is False
    parser.advance()
    eof = parser.peek()
    assert parser.at_end() is True
    assert parser.advance() is eof
    assert parser.expect("EOF") is eof
    assert parser.match("IDENT") is False
    assert parser.peek() is eof
    assert parser.current == 1


@pytest.mark.parametrize("entrada", [[], tokens(("IDENT", "x"))[:-1]])
def test_lista_precisa_terminar_em_eof(entrada):
    with pytest.raises(ValueError, match="EOF"):
        Parser(entrada)


@pytest.mark.parametrize(("expressao", "esperado"), [
    (
        [("INT_LITERAL", "2"), ("PLUS", "+"), ("INT_LITERAL", "3"),
         ("STAR", "*"), ("INT_LITERAL", "4")],
        Binaria("+", Inteiro(2), Binaria("*", Inteiro(3), Inteiro(4))),
    ),
    (
        [("LPAREN", "("), ("INT_LITERAL", "2"), ("PLUS", "+"),
         ("INT_LITERAL", "3"), ("RPAREN", ")"), ("STAR", "*"), ("INT_LITERAL", "4")],
        Binaria("*", Binaria("+", Inteiro(2), Inteiro(3)), Inteiro(4)),
    ),
    (
        [("INT_LITERAL", "10"), ("MINUS", "-"), ("INT_LITERAL", "3"),
         ("MINUS", "-"), ("INT_LITERAL", "2")],
        Binaria("-", Binaria("-", Inteiro(10), Inteiro(3)), Inteiro(2)),
    ),
    ([("IDENT", "y")], Variavel("y")),
    (
        [("INT_LITERAL", "20"), ("SLASH", "/"), ("INT_LITERAL", "2"),
         ("SLASH", "/"), ("INT_LITERAL", "5")],
        Binaria("/", Binaria("/", Inteiro(20), Inteiro(2)), Inteiro(5)),
    ),
    (
        [("INT_LITERAL", "1"), ("SLASH", "/"), ("INT_LITERAL", "0")],
        Binaria("/", Inteiro(1), Inteiro(0)),
    ),
])
def test_exemplos_constroem_ast_sem_executar(expressao, esperado):
    entrada = [("KW_PRINT", "print"), ("LPAREN", "(")]
    entrada += expressao + [("RPAREN", ")"), ("SEMICOLON", ";")]
    parser = Parser(tokens(*entrada))
    assert parser.programa() == Programa([Saida(esperado)])
    assert parser.at_end()


def test_programa_vazio():
    parser = Parser(tokens())
    assert parser.programa() == Programa([])
    assert parser.at_end()


def test_sequencia_de_declaracao_atribuicao_e_saida():
    parser = Parser(tokens(
        ("KW_INT", "int"), ("IDENT", "x"), ("SEMICOLON", ";"),
        ("IDENT", "x"), ("ASSIGN", "="), ("INT_LITERAL", "2"), ("SEMICOLON", ";"),
        ("KW_PRINT", "print"), ("LPAREN", "("), ("IDENT", "x"),
        ("RPAREN", ")"), ("SEMICOLON", ";"),
    ))
    assert parser.programa() == Programa([
        Declaracao("x"), Atribuicao("x", Inteiro(2)), Saida(Variavel("x")),
    ])
    assert parser.at_end()


def test_para_no_primeiro_erro_com_token_e_posicao():
    entrada = tokens(
        ("KW_PRINT", "print"), ("LPAREN", "("), ("INT_LITERAL", "2"),
        ("PLUS", "+"), ("RPAREN", ")"), ("SEMICOLON", ";"),
        ("KW_PRINT", "print"), ("LPAREN", "("), ("RPAREN", ")"),
    )
    entrada[4].line, entrada[4].column = 2, 7
    parser = Parser(entrada)
    with pytest.raises(ExceptionSyntax) as resultado:
        parser.programa()
    erro = resultado.value
    assert erro.token is entrada[4]
    assert (erro.line, erro.column) == (2, 7)
    assert erro.expected == ("INT_LITERAL", "IDENT", "LPAREN")
    assert parser.peek() is entrada[4]


@pytest.mark.parametrize("entrada", [
    [("KW_INT", "int"), ("IDENT", "x")],
    [("KW_INT", "int"), ("SEMICOLON", ";")],
    [("IDENT", "x"), ("INT_LITERAL", "2"), ("SEMICOLON", ";")],
    [("IDENT", "x"), ("ASSIGN", "="), ("SEMICOLON", ";")],
    [("KW_PRINT", "print"), ("LPAREN", "("), ("INT_LITERAL", "2"),
     ("INT_LITERAL", "3"), ("RPAREN", ")"), ("SEMICOLON", ";")],
    [("KW_PRINT", "print"), ("LPAREN", "("), ("MINUS", "-"),
     ("INT_LITERAL", "2"), ("RPAREN", ")"), ("SEMICOLON", ";")],
    [("KW_IF", "if")], [("KW_WHILE", "while")], [("LBRACE", "{")],
    [("KW_PRINT", "print"), ("LPAREN", "("), ("INT_LITERAL", "2"),
     ("RPAREN", ")"), ("SEMICOLON", ";"), ("INT_LITERAL", "3")],
])
def test_rejeita_sintaxe_invalida_e_nao_ignora_sobra(entrada):
    with pytest.raises(ExceptionSyntax):
        Parser(tokens(*entrada)).programa()


@pytest.mark.parametrize(("source", "esperado"), [
    (
        "print(2 + 3 * 4);",
        Programa([Saida(Binaria("+", Inteiro(2), Binaria("*", Inteiro(3), Inteiro(4))))]),
    ),
    (
        "print((2 + 3) * 4);",
        Programa([Saida(Binaria("*", Binaria("+", Inteiro(2), Inteiro(3)), Inteiro(4)))]),
    ),
    (
        "print(10 - 3 - 2);",
        Programa([Saida(Binaria("-", Binaria("-", Inteiro(10), Inteiro(3)), Inteiro(2)))]),
    ),
    ("print(y);", Programa([Saida(Variavel("y"))])),
    ("", Programa([])),
])
def test_exemplos_do_professor_com_lexer_real(source, esperado):
    entrada, diagnostics = Lexer(source).scan_tokens()
    assert diagnostics == []
    parser = Parser(entrada)
    assert parser.programa() == esperado
    assert parser.at_end()


def test_erro_do_professor_com_lexer_real():
    entrada, diagnostics = Lexer("print(2 + ); print(3 + );").scan_tokens()
    assert diagnostics == []
    parser = Parser(entrada)
    with pytest.raises(ExceptionSyntax) as resultado:
        parser.programa()
    erro = resultado.value
    assert (erro.line, erro.column) == (1, 11)
    assert erro.token.type == "RPAREN"
    assert parser.peek() is erro.token


def test_programa_completo_com_lexer_real():
    entrada, diagnostics = Lexer("int x; x = 2 + 3 * 4; print(x);").scan_tokens()
    assert diagnostics == []
    assert Parser(entrada).programa() == Programa([
        Declaracao("x"),
        Atribuicao("x", Binaria("+", Inteiro(2), Binaria("*", Inteiro(3), Inteiro(4)))),
        Saida(Variavel("x")),
    ])


@pytest.mark.parametrize(("source", "codigo", "trecho"), [
    ("print(1 / 0);", 0, "Binaria(/)"),
    ("print(2 + );", 1, "linha 1, coluna 11"),
    ("@print(2);", 1, "Erro lexico na linha 1, coluna 1"),
])
def test_execucao_do_arquivo_sem_dependencias_externas(tmp_path, capsys, source, codigo, trecho):
    arquivo = tmp_path / "programa.min"
    arquivo.write_text(source, encoding="utf-8")
    assert main(["main.py", str(arquivo)]) == codigo
    saida = capsys.readouterr()
    if codigo == 0:
        assert trecho in saida.out
        assert saida.err == ""
    else:
        assert saida.out == ""
        assert trecho in saida.err


def test_comando_sem_arquivo_informa_uso(capsys):
    assert main(["main.py"]) == 2
    assert "Uso: python main.py <arquivo.min>" in capsys.readouterr().err


def test_arquivo_inexistente_informa_erro(tmp_path, capsys):
    assert main(["main.py", str(tmp_path / "inexistente.min")]) == 2
    assert "Erro ao ler arquivo" in capsys.readouterr().err
