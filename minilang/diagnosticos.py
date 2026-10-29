class ExceptionSyntax(SyntaxError):
    def __init__(self, token, expected, line=None, column=None):
        self.token = token
        self.expected = (expected,) if isinstance(expected, str) else tuple(expected)
        self.line = token.line if line is None else line
        self.column = token.column if column is None else column

        message = (
            f"Erro sintatico na linha {self.line}, coluna {self.column}: "
            f"encontrado {token.type} ({token.lexeme!r}); "
            f"esperado: {', '.join(self.expected)}"
        )
        super().__init__(message)
