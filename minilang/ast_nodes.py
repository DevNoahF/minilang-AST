from dataclasses import dataclass, field

@dataclass
class Programa:
    itens: list


@dataclass
class Declaracao:
    nome: str
    inicializador: object = None
    tipo: str = "int"
    token: object = field(default=None, compare=False)
    simbolo: object = field(default=None, compare=False)


@dataclass
class Atribuicao:
    nome: str
    expressao: object
    token: object = field(default=None, compare=False)
    simbolo: object = field(default=None, compare=False)


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
    senao: Bloco = None
    token: object = field(default=None, compare=False)


@dataclass
class Enquanto:
    condicao: object
    corpo: Bloco
    token: object = field(default=None, compare=False)


@dataclass
class Para:
    inicializacao: object
    condicao: object
    atualizacao: object
    corpo: Bloco
    token: object = field(default=None, compare=False)


@dataclass
class Binaria:
    operador: str
    esquerda: object
    direita: object
    token: object = field(default=None, compare=False)
    tipo: str = field(default=None, compare=False)


@dataclass
class Variavel:
    nome: str
    token: object = field(default=None, compare=False)
    simbolo: object = field(default=None, compare=False)
    tipo: str = field(default=None, compare=False)


@dataclass
class Inteiro:
    valor: int
    token: object = field(default=None, compare=False)
    tipo: str = field(default=None, compare=False)


@dataclass
class Booleano:
    valor: bool
    token: object = field(default=None, compare=False)
    tipo: str = field(default=None, compare=False)


def formatar_ast(no, nivel=0, lado=None, anotada=False):
    filhos = []
    if isinstance(no, Programa):
        rotulo = "Programa"
        filhos = [(None, item) for item in no.itens]
    elif isinstance(no, Declaracao):
        rotulo = f"Declaracao({no.nome})"
        if anotada:
            rotulo += f": {no.tipo} -> {no.simbolo.id if no.simbolo else 'ERRO'}"
        if no.inicializador is not None:
            filhos = [(None, no.inicializador)]
    elif isinstance(no, Atribuicao):
        rotulo = f"Atribuicao({no.nome})"
        if anotada:
            rotulo += f" -> {no.simbolo.id if no.simbolo else 'ERRO'}"
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
        if no.senao is not None:
            filhos.append(("Senao", no.senao))
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
        if anotada:
            rotulo += f": {no.tipo}"
        filhos = [("E", no.esquerda), ("D", no.direita)]
    elif isinstance(no, Variavel):
        rotulo = f"Variavel({no.nome})"
        if anotada:
            rotulo += f" -> {no.simbolo.id if no.simbolo else 'ERRO'}: {no.tipo}"
    elif isinstance(no, Inteiro):
        rotulo = f"Inteiro({no.valor})"
        if anotada:
            rotulo += f": {no.tipo}"
    elif isinstance(no, Booleano):
        rotulo = f"Booleano({no.valor})"
        if anotada:
            rotulo += f": {no.tipo}"
    else:
        raise TypeError(f"No de AST desconhecido: {type(no).__name__}")

    prefixo = f"{lado}: " if lado else ""
    linhas = ["  " * nivel + prefixo + rotulo]
    for lado_filho, filho in filhos:
        linhas.append(formatar_ast(filho, nivel + 1, lado_filho, anotada))
    return "\n".join(linhas)
