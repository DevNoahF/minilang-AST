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


def formatar_ast(no, nivel=0, lado=None):
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

    prefixo = f"{lado}: " if lado else ""
    linhas = ["  " * nivel + prefixo + rotulo]
    for indice, filho in enumerate(filhos):
        lado_filho = ("E", "D")[indice] if isinstance(no, Binaria) else None
        linhas.append(formatar_ast(filho, nivel + 1, lado_filho))
    return "\n".join(linhas)
