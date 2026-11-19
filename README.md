# MiniLang: análise sintática e semântica

- Noah Veri de Morais Franco - 2014803
- Leonardo Perin Andreozi - 1995746
- Gustavo Rosa de Jesus - 2012734
- Joaquim Pedro Augusto de Oliveira - 1993926

O parser da Aula 09 constrói a AST (Árvore Sintática Abstrata). A etapa da
Aula 10 percorre essa árvore e verifica declarações, escopos e tipos. O
programa analisado **não é executado**. O lexer foi reaproveitado do trabalho
anterior do grupo.

## Organização

- `minilang/`: lexer, parser, AST, análise semântica e diagnósticos.
- `tests/`: testes automatizados.
- `examples/`: exemplos, incluindo `aula10.min` (slide 41).
- `main.py`: entrada para executar o analisador.

## Executar

Com Python 3 instalado, abra o terminal na pasta `minilang-AST` e execute:

```text
python main.py examples/aula10.min
```

O terminal mostra as tabelas de símbolos, a AST anotada e os diagnósticos.
No exemplo da Aula 10, as tabelas contêm:

```text
Escopo 0 (global)
  s0  total  int  1:5
Escopo 1 (bloco, pai: 0)
  s1  limite  int  4:9
  s2  acima  bool  5:10
```

Cada `s` identifica uma declaração. Por exemplo, na AST anotada,
`Variavel(total) -> s0: int` quer dizer que aquele uso de `total` aponta para
a declaração da linha 1. `Binaria(>): bool` indica o tipo da comparação.
Nos filhos de uma operação binária, `E` é o operando à esquerda e `D` à direita.

Os quatro erros do exemplo são:

```text
E_OPERANDOS na linha 8, coluna 20: operador '+' não aceita int e bool
E_ATRIBUICAO na linha 9, coluna 5: 'total' é int, mas a expressão é bool
E_NOME na linha 11, coluna 7: 'acima' não declarado neste ponto
E_REDECLARACAO na linha 12, coluna 5: 'total' já declarado em 1:5
```

O código de saída é `1` quando há erros e `0` quando a análise termina sem
erros. Um erro semântico não interrompe a busca pelos próximos erros.

Para analisar outro programa, substitua o caminho pelo seu arquivo `.min`.

## Regras principais

- Cada declaração entra somente no escopo atual. Declarar de novo no mesmo
  escopo é erro; a primeira declaração continua valendo.
- Para usar uma variável, a busca começa no escopo atual e segue para os pais.
  Ao sair de um bloco, a tabela dele continua na saída, mas deixa de participar
  da busca. Assim, uma declaração interna pode ocultar uma externa.
- `int` e `bool` são tipos distintos. `+`, `-`, `*` e `/` exigem dois `int` e
  retornam `int`. `<`, `<=`, `>` e `>=` exigem dois `int` e retornam `bool`.
  `==` e `!=` exigem operandos do mesmo tipo. `AND` e `OR` exigem dois `bool`.
- `print` aceita `int` ou `bool`. Condições de `if`, `while` e `for` devem ser
  `bool`. São aceitos `true` e `false` (também `True` e `False`).
- Uma expressão com erro recebe tipo `ERRO`. Isso evita repetir o mesmo
  diagnóstico numa atribuição, sem esconder outros erros independentes.

O parser também reconhece blocos, `if`/`else`, `while` e `for`:

```text
python main.py examples/controle_fluxo.min
```

## Exemplo de erro

```text
python main.py examples/erro_sintatico.min
```

A entrada `print(2 + );` interrompe a análise no primeiro erro e informa:

```text
Erro sintatico na linha 1, coluna 11: encontrado RPAREN (')'); esperado: INT_LITERAL, IDENT, LPAREN, KW_TRUE, KW_FALSE
```

## Testes

```text
python -m pip install -r requirements.txt
python -m pytest -v
```

Também é possível executar `pytest -v`; o `pytest.ini` configura os imports.
A pasta `.pytest_aula10_tmp/` é exclusiva dos testes e recriada a cada execução.

Os testes verificam o parser antigo, o exemplo do slide 41, vínculos dos nomes,
escopos, tipos e diagnósticos com posição.
