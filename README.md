# Analisador Sintático da MiniLang

Trabalho 02: parser descendente recursivo que reconhece declarações `int`,
atribuições, `print` e expressões com `+`, `-`, `*`, `/` e parênteses.
Constrói uma AST (Árvore Sintática Abstrata), respeitando precedência e
associatividade à esquerda, sem executar o programa ou fazer análise semântica.
O lexer foi reaproveitado do trabalho anterior do grupo.

## Organização

- `minilang/`: lexer, parser, AST e diagnósticos.
- `tests/`: testes automatizados.
- `examples/`: exemplos de programa válido e erro sintático.
- `main.py`: entrada para executar o analisador.

## Executar

Com Python 3 instalado, abra o terminal na pasta `minilang-AST` e execute:

```text
python main.py examples/programa.min
```

A árvore sintática (AST) do arquivo informado será exibida no terminal:

```text
Programa
  Declaracao(x)
  Atribuicao(x)
    Binaria(+)
      E: Inteiro(2)
      D: Binaria(*)
        E: Inteiro(3)
        D: Inteiro(4)
  Saida
    Variavel(x)
```

Nos filhos de cada operação binária, `E` indica o operando à esquerda e `D`
indica o operando à direita.

Para analisar outro programa, substitua o caminho pelo seu arquivo `.min`.

## Exemplo de erro

```text
python main.py examples/erro_sintatico.min
```

A entrada `print(2 + );` interrompe a análise no primeiro erro e informa:

```text
Erro sintatico na linha 1, coluna 11: encontrado RPAREN (')'); esperado: INT_LITERAL, IDENT, LPAREN
```

## Testes

```text
python -m pip install -r requirements.txt
python -m pytest -v
```

Também é possível executar `pytest -v`; o `pytest.ini` configura os imports.
A pasta `.pytest_tmp/` é exclusiva dos testes e recriada a cada execução.

Os testes verificam os exemplos do professor, a AST, precedência,
associatividade, consumo dos tokens até EOF e diagnósticos com posição.
