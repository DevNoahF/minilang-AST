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
class Inteiro:
    valor: int


@dataclass
class Variavel:
    nome: str


@dataclass
class Binaria:
    esquerda: object
    operador: str
    direita: object


def mostrar_ast(no):
    def rotulo(atual):
        if isinstance(atual, Programa):
            return "Programa"
        if isinstance(atual, Declaracao):
            return f"Declaracao({atual.nome})"
        if isinstance(atual, Atribuicao):
            return f"Atribuicao({atual.nome})"
        if isinstance(atual, Saida):
            return "Saida"
        if isinstance(atual, Inteiro):
            return f"Inteiro({atual.valor})"
        if isinstance(atual, Variavel):
            return f"Variavel({atual.nome})"
        if isinstance(atual, Binaria):
            return f"Binaria({atual.operador})"
        raise TypeError(f"nó de AST não reconhecido: {type(atual).__name__}")

    def filhos(atual):
        if isinstance(atual, Programa):
            return atual.itens
        if isinstance(atual, Atribuicao):
            return [atual.expressao]
        if isinstance(atual, Saida):
            return [atual.expressao]
        if isinstance(atual, Binaria):
            return [atual.esquerda, atual.direita]
        return []

    def imprimir(atual, nivel):
        print(f"{'  ' * nivel}{rotulo(atual)}")
        for filho in filhos(atual):
            imprimir(filho, nivel + 1)

    imprimir(no, 0)
