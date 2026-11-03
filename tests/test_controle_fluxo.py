from main import run

# O retorno 0 indica que o programa foi analisado sem erros.

def test_if():
    codigo = "if (1 < 3) { print(1); }"
    assert run(codigo) == 0


def test_while():
    codigo = "int x; x = 0; while (x < 3) { x = x + 1; }"
    assert run(codigo) == 0


def test_for():
    codigo = "for (int i = 0; i < 3; i = i + 1) { print(i); }"
    assert run(codigo) == 0
