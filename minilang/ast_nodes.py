"""AST implementada pelo grupo para integrar o lexer antigo ao parser."""

from dataclasses import dataclass


@dataclass
class Programa:
    itens: list


@dataclass
class Declaracao:
    nome: str


@dataclass
class Atribuicao:
    nome: str
    expressao: object


@dataclass
class Saida:
    expressao: object


@dataclass
class Binaria:
    operador: str
    esquerda: object
    direita: object


@dataclass
class Variavel:
    nome: str


@dataclass
class Inteiro:
    valor: int


def formatar_ast(no, nivel=0):
    """Mostra a estrutura da AST sem executar o programa."""
    filhos = []
    if isinstance(no, Programa):
        rotulo = "Programa"
        filhos = no.itens
    elif isinstance(no, Declaracao):
        rotulo = f"Declaracao({no.nome})"
    elif isinstance(no, Atribuicao):
        rotulo = f"Atribuicao({no.nome})"
        filhos = [no.expressao]
    elif isinstance(no, Saida):
        rotulo = "Saida"
        filhos = [no.expressao]
    elif isinstance(no, Binaria):
        rotulo = f"Binaria({no.operador})"
        filhos = [no.esquerda, no.direita]
    elif isinstance(no, Variavel):
        rotulo = f"Variavel({no.nome})"
    elif isinstance(no, Inteiro):
        rotulo = f"Inteiro({no.valor})"
    else:
        raise TypeError(f"No de AST desconhecido: {type(no).__name__}")

    linhas = ["  " * nivel + rotulo]
    linhas.extend(formatar_ast(filho, nivel + 1) for filho in filhos)
    return "\n".join(linhas)
