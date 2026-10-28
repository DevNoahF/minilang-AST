class ExceptionSyntax(Exception):
    def __init__(self, token, expected, line, column):
        self.token = token
        self.expected = expected
        self.line = line
        self.column = column

        message = (
            f"---Syntax error--- line: {self.line}"
            f"---Syntax error--- column:  {self.column}\n"
            f"Token find: {self.token.value!r}\n"
            f"Expected: {self.expected}"
        )
        super().__init__(message)