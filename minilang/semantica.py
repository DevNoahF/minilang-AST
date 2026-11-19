"""Análise de nomes, escopos e tipos da MiniLang."""

from dataclasses import dataclass, field

from .ast_nodes import (
    Atribuicao, Binaria, Bloco, Booleano, Condicional, Declaracao,
    Enquanto, Inteiro, Para, Programa, Saida, Variavel,
)


ERRO = "ERRO"


@dataclass
class Simbolo:
    id: str
    nome: str
    tipo: str
    escopo: int
    token: object


@dataclass
class Escopo:
    id: int
    pai: object = None
    simbolos: dict = field(default_factory=dict)


@dataclass
class Diagnostico:
    codigo: str
    mensagem: str
    linha: int
    coluna: int

    def __str__(self):
        return f"{self.codigo} na linha {self.linha}, coluna {self.coluna}: {self.mensagem}"


class AnalisadorSemantico:
    def __init__(self):
        global_ = Escopo(0)
        self.escopos = [global_]
        self.atual = global_
        self.diagnosticos = []

    def analisar(self, programa):
        self.visitar(programa)
        return self

    def erro(self, codigo, mensagem, token):
        self.diagnosticos.append(Diagnostico(
            codigo, mensagem, token.line, token.column,
        ))

    def abrir_escopo(self):
        novo = Escopo(len(self.escopos), self.atual)
        self.escopos.append(novo)
        self.atual = novo

    def fechar_escopo(self):
        self.atual = self.atual.pai

    def resolver(self, nome, token):
        escopo = self.atual
        while escopo is not None:
            if nome in escopo.simbolos:
                return escopo.simbolos[nome]
            escopo = escopo.pai
        self.erro("E_NOME", f"'{nome}' não declarado neste ponto", token)
        return None

    def visitar(self, no):
        if isinstance(no, Programa):
            for item in no.itens:
                self.visitar(item)
        elif isinstance(no, Bloco):
            self.abrir_escopo()
            for item in no.itens:
                self.visitar(item)
            self.fechar_escopo()
        elif isinstance(no, Declaracao):
            anterior = self.atual.simbolos.get(no.nome)
            if anterior is not None:
                self.erro(
                    "E_REDECLARACAO",
                    f"'{no.nome}' já declarado em {anterior.token.line}:{anterior.token.column}",
                    no.token,
                )
            else:
                simbolo = Simbolo(
                    f"s{sum(len(e.simbolos) for e in self.escopos)}",
                    no.nome, no.tipo, self.atual.id, no.token,
                )
                self.atual.simbolos[no.nome] = simbolo
                no.simbolo = simbolo
            if no.inicializador is not None:
                tipo = self.tipo_expr(no.inicializador)
                if anterior is None and tipo != ERRO and tipo != no.tipo:
                    self.erro(
                        "E_ATRIBUICAO",
                        f"'{no.nome}' é {no.tipo}, mas a expressão é {tipo}", no.token,
                    )
        elif isinstance(no, Atribuicao):
            no.simbolo = self.resolver(no.nome, no.token)
            tipo = self.tipo_expr(no.expressao)
            if no.simbolo is not None and tipo != ERRO and tipo != no.simbolo.tipo:
                self.erro(
                    "E_ATRIBUICAO",
                    f"'{no.nome}' é {no.simbolo.tipo}, mas a expressão é {tipo}", no.token,
                )
        elif isinstance(no, Saida):
            self.tipo_expr(no.expressao)
        elif isinstance(no, Condicional):
            self.verificar_condicao(no.condicao, no.token)
            self.visitar(no.entao)
            if no.senao is not None:
                self.visitar(no.senao)
        elif isinstance(no, Enquanto):
            self.verificar_condicao(no.condicao, no.token)
            self.visitar(no.corpo)
        elif isinstance(no, Para):
            self.abrir_escopo()
            if no.inicializacao is not None:
                self.visitar(no.inicializacao)
            if no.condicao is not None:
                self.verificar_condicao(no.condicao, no.token)
            if no.atualizacao is not None:
                self.visitar(no.atualizacao)
            self.visitar(no.corpo)
            self.fechar_escopo()
        else:
            raise TypeError(f"Nó desconhecido: {type(no).__name__}")

    def verificar_condicao(self, expressao, token):
        tipo = self.tipo_expr(expressao)
        if tipo != ERRO and tipo != "bool":
            self.erro("E_CONDICAO", f"condição deve ser bool, mas é {tipo}", token)

    def tipo_expr(self, no):
        if isinstance(no, Inteiro):
            no.tipo = "int"
        elif isinstance(no, Booleano):
            no.tipo = "bool"
        elif isinstance(no, Variavel):
            no.simbolo = self.resolver(no.nome, no.token)
            no.tipo = no.simbolo.tipo if no.simbolo is not None else ERRO
        elif isinstance(no, Binaria):
            esquerda = self.tipo_expr(no.esquerda)
            direita = self.tipo_expr(no.direita)
            if ERRO in (esquerda, direita):
                no.tipo = ERRO
            elif no.operador in ("+", "-", "*", "/") and (esquerda, direita) == ("int", "int"):
                no.tipo = "int"
            elif no.operador in ("<", "<=", ">", ">=") and (esquerda, direita) == ("int", "int"):
                no.tipo = "bool"
            elif no.operador in ("==", "!=") and esquerda == direita:
                no.tipo = "bool"
            elif no.operador in ("AND", "OR") and (esquerda, direita) == ("bool", "bool"):
                no.tipo = "bool"
            else:
                no.tipo = ERRO
                self.erro(
                    "E_OPERANDOS",
                    f"operador '{no.operador}' não aceita {esquerda} e {direita}", no.token,
                )
        else:
            raise TypeError(f"Expressão desconhecida: {type(no).__name__}")
        return no.tipo


def formatar_tabelas(escopos):
    linhas = []
    for escopo in escopos:
        descricao = "global" if escopo.pai is None else f"bloco, pai: {escopo.pai.id}"
        linhas.append(f"Escopo {escopo.id} ({descricao})")
        if not escopo.simbolos:
            linhas.append("  (sem declarações)")
        for simbolo in escopo.simbolos.values():
            linhas.append(
                f"  {simbolo.id}  {simbolo.nome}  {simbolo.tipo}  "
                f"{simbolo.token.line}:{simbolo.token.column}"
            )
    return "\n".join(linhas)
