from dataclasses import dataclass

@dataclass
class Programa:
    itens: list


@dataclass
class Declaracao:
    nome: str
    inicializador: object = None


@dataclass
class Atribuicao:
    nome: str
    expressao: object


@dataclass
class Saida:
    expressao: object


@dataclass
class Bloco:
    itens: list


@dataclass
class Condicional:
    condicao: object
    entao: Bloco


@dataclass
class Enquanto:
    condicao: object
    corpo: Bloco


@dataclass
class Para:
    inicializacao: object
    condicao: object
    atualizacao: object
    corpo: Bloco


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
        filhos = [(None, item) for item in no.itens]
    elif isinstance(no, Declaracao):
        rotulo = f"Declaracao({no.nome})"
        if no.inicializador is not None:
            filhos = [(None, no.inicializador)]
    elif isinstance(no, Atribuicao):
        rotulo = f"Atribuicao({no.nome})"
        filhos = [(None, no.expressao)]
    elif isinstance(no, Saida):
        rotulo = "Saida"
        filhos = [(None, no.expressao)]
    elif isinstance(no, Bloco):
        rotulo = "Bloco"
        filhos = [(None, item) for item in no.itens]
    elif isinstance(no, Condicional):
        rotulo = "Condicional"
        filhos = [("Condicao", no.condicao), ("Entao", no.entao)]
    elif isinstance(no, Enquanto):
        rotulo = "Enquanto"
        filhos = [("Condicao", no.condicao), ("Corpo", no.corpo)]
    elif isinstance(no, Para):
        rotulo = "Para"
        filhos = [
            ("Inicializacao", no.inicializacao),
            ("Condicao", no.condicao),
            ("Atualizacao", no.atualizacao),
            ("Corpo", no.corpo),
        ]
        filhos = [(lado, filho) for lado, filho in filhos if filho is not None]
    elif isinstance(no, Binaria):
        rotulo = f"Binaria({no.operador})"
        filhos = [("E", no.esquerda), ("D", no.direita)]
    elif isinstance(no, Variavel):
        rotulo = f"Variavel({no.nome})"
    elif isinstance(no, Inteiro):
        rotulo = f"Inteiro({no.valor})"
    else:
        raise TypeError(f"No de AST desconhecido: {type(no).__name__}")

    prefixo = f"{lado}: " if lado else ""
    linhas = ["  " * nivel + prefixo + rotulo]
    for lado_filho, filho in filhos:
        linhas.append(formatar_ast(filho, nivel + 1, lado_filho))
    return "\n".join(linhas)
