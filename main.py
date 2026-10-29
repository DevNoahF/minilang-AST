"""Executa o lexer e o parser, exibindo a AST ou os diagnosticos."""

import sys
from pathlib import Path

from minilang import Lexer, Parser
from minilang.ast_nodes import formatar_ast
from minilang.diagnosticos import ExceptionSyntax


def run(source):
    tokens, diagnostics = Lexer(source).scan_tokens()
    if diagnostics:
        for diagnostic in diagnostics:
            print(
                f"Erro lexico na linha {diagnostic.line}, "
                f"coluna {diagnostic.column}: {diagnostic.message}",
                file=sys.stderr,
            )
        return 1

    try:
        ast = Parser(tokens).programa()
    except ExceptionSyntax as error:
        print(error, file=sys.stderr)
        return 1

    print(formatar_ast(ast))
    return 0


def main(argv):
    if len(argv) != 2:
        print("Uso: python main.py <arquivo.min>", file=sys.stderr)
        return 2
    try:
        source = Path(argv[1]).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        print(f"Erro ao ler arquivo: {error}", file=sys.stderr)
        return 2
    return run(source)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
