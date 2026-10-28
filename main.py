"""Ponto de entrada do analisador sintático da MiniLang."""

import sys

from minilang.ast_nodes import mostrar_ast
from minilang.lexer import Lexer
from minilang.parser import ErroSintatico, Parser


def run(source):
    lexer = Lexer(source)
    tokens, diagnostics = lexer.scan_tokens()

    for diagnostic in diagnostics:
        print(
            f"Erro léxico em {diagnostic.line}:{diagnostic.column}: "
            f"{diagnostic.message}",
            file=sys.stderr,
        )

    try:
        arvore = Parser(tokens).programa()
    except ErroSintatico as error:
        print(error, file=sys.stderr)
        return 1

    mostrar_ast(arvore)
    return 1 if diagnostics else 0


def main(argv):
    if len(argv) != 2:
        print("uso: python main.py <arquivo.min>", file=sys.stderr)
        return 1

    path = argv[1]
    try:
        with open(path, "r", encoding="utf-8") as handle:
            source = handle.read()
    except OSError as error:
        print(f"erro ao abrir '{path}': {error}", file=sys.stderr)
        return 1

    return run(source)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
