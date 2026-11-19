from pathlib import Path

from minilang import Lexer, Parser
from minilang.ast_nodes import formatar_ast
from minilang.semantica import AnalisadorSemantico, formatar_tabelas


def analisar(source):
    tokens, erros_lexicos = Lexer(source).scan_tokens()
    assert erros_lexicos == []
    ast = Parser(tokens).programa()
    return ast, AnalisadorSemantico().analisar(ast)


def test_exemplo_do_slide_41():
    source = (Path(__file__).parents[1] / "examples" / "aula10.min").read_text(encoding="utf-8")
    ast, analise = analisar(source)

    assert [(d.codigo, d.linha, d.coluna) for d in analise.diagnosticos] == [
        ("E_OPERANDOS", 8, 20),
        ("E_ATRIBUICAO", 9, 5),
        ("E_NOME", 11, 7),
        ("E_REDECLARACAO", 12, 5),
    ]
    assert [(s.nome, s.tipo, s.token.line, s.token.column)
            for e in analise.escopos for s in e.simbolos.values()] == [
        ("total", "int", 1, 5),
        ("limite", "int", 4, 9),
        ("acima", "bool", 5, 10),
    ]
    assert ast.itens[2].itens[3].expressao.tipo == "bool"  # total > limite
    assert ast.itens[2].itens[4].expressao.tipo == "ERRO"  # limite + acima
    assert ast.itens[2].itens[3].simbolo is analise.escopos[1].simbolos["acima"]
    texto = formatar_ast(ast, anotada=True)
    assert "Atribuicao(acima) -> s2" in texto
    assert "Variavel(total) -> s0: int" in texto
    assert "Binaria(>): bool" in texto
    assert "Escopo 1" in formatar_tabelas(analise.escopos)


def test_sombreamento_comeca_apos_declaracao_local():
    ast, analise = analisar("int x; { print(x); bool x; print(x); } print(x);")
    assert analise.diagnosticos == []
    global_ = analise.escopos[0].simbolos["x"]
    local = analise.escopos[1].simbolos["x"]
    bloco = ast.itens[1]
    assert bloco.itens[0].expressao.simbolo is global_
    assert bloco.itens[2].expressao.simbolo is local
    assert ast.itens[2].expressao.simbolo is global_


def test_erros_independentes_sem_cascata():
    _, analise = analisar("int x;\nz = y + 1;")
    assert [(d.codigo, d.linha, d.coluna) for d in analise.diagnosticos] == [
        ("E_NOME", 2, 1), ("E_NOME", 2, 5),
    ]


def test_tipos_booleanos_e_condicoes():
    ast, analise = analisar(
        "bool ativo = true; int x = 1; "
        "print(ativo AND (x < 3)); "
        "if (ativo) { print(false); } else { print(x); }"
    )
    assert analise.diagnosticos == []
    assert ast.itens[2].expressao.tipo == "bool"
    assert len(analise.escopos) == 3


def test_igualdade_e_condicao_invalidas():
    _, analise = analisar("print(1 == true); if (1) { print(2); }")
    assert [d.codigo for d in analise.diagnosticos] == ["E_OPERANDOS", "E_CONDICAO"]


def test_redeclaracao_preserva_primeiro_simbolo_e_ordem_dos_usos():
    ast, analise = analisar("print(x); int x; bool x; print(x);")
    assert [d.codigo for d in analise.diagnosticos] == ["E_NOME", "E_REDECLARACAO"]
    assert analise.escopos[0].simbolos["x"].tipo == "int"
    assert ast.itens[3].expressao.simbolo is analise.escopos[0].simbolos["x"]


def test_variavel_do_for_sai_de_escopo():
    _, analise = analisar(
        "for (int i = 0; i < 2; i = i + 1) { print(i); } print(i);"
    )
    assert [(d.codigo, d.coluna) for d in analise.diagnosticos] == [("E_NOME", 55)]
