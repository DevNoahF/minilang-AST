class Lexer:
    def __init__(self, source):
        self.source = source.replace("\r\n", "\n")

        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
        self.start_line = 1
        self.start_column = 1

        self.tokens = []
        self.diagnostics = []

    def scan_tokens(self):
        while not self.at_end():
            self.start = self.current
            self.start_line = self.line
            self.start_column = self.column
            self.scan_token()

        eof = Token(TokenType.EOF, "", self.line, self.column)
        self.tokens.append(eof)
        return self.tokens, self.diagnostics


    def scan_token(self):
        if self.peek() == "/" and self.peek_next() == "/":
            self.advance()
            self.advance()
            self.line_comment()
            return

        c = self.advance()

        if is_identifier_start(c):
            self.identifier()
        elif is_ascii_digit(c):
            self.number()
        elif c == "/":
            self.add_token(TokenType.SLASH)
        elif c == "=":
            if self.match("="):
                self.add_token(TokenType.EQUAL_EQUAL)
            else:
                self.add_token(TokenType.ASSIGN)
        elif c == "!":
            if self.match("="):
                self.add_token(TokenType.BANG_EQUAL)
            else:
                self.report_invalid_character(c)
        elif c == "<":
            if self.match("="):
                self.add_token(TokenType.LESS_EQUAL)
            else:
                self.add_token(TokenType.LESS)
        elif c == ">":
            if self.match("="):
                self.add_token(TokenType.GREATER_EQUAL)
            else:
                self.add_token(TokenType.GREATER)
        elif c == "+":
            self.add_token(TokenType.PLUS)
        elif c == "-":
            self.add_token(TokenType.MINUS)
        elif c == "*":
            self.add_token(TokenType.STAR)
        elif c == "(":
            self.add_token(TokenType.LPAREN)
        elif c == ")":
            self.add_token(TokenType.RPAREN)
        elif c == ";":
            self.add_token(TokenType.SEMICOLON)
        elif c == "{":
            self.add_token(TokenType.LBRACE)
        elif c == "}":
            self.add_token(TokenType.RBRACE)
        elif is_whitespace(c):
            while is_whitespace(self.peek()):
                self.advance()
        else:
            self.report_invalid_character(c)


    def at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        c = self.source[self.current]
        self.current += 1

        if c == "\r" or c == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        return c

    def peek(self):
        if self.at_end():
            return "\0"
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def match(self, expected):
        if self.at_end() or self.source[self.current] != expected:
            return False

        self.advance()
        return True


    def add_token(self, type_):
        lexeme = self.source[self.start:self.current]
        token = Token(type_, lexeme, self.start_line, self.start_column)
        self.tokens.append(token)


    def identifier(self):
        while is_identifier_part(self.peek()):
            self.advance()

        lexeme = self.source[self.start:self.current]
        type_ = KEYWORDS.get(lexeme, TokenType.IDENT)
        self.add_token(type_)

    def number(self):
        while is_ascii_digit(self.peek()):
            self.advance()
        self.add_token(TokenType.INT_LITERAL)

    def line_comment(self):
        while not self.at_end() and self.peek() != "\r" and self.peek() != "\n":
            self.advance()


    def report_invalid_character(self, character):
        message = f"simbolo invalido: {character!r}"
        diagnostic = Diagnostic(
            character,
            self.start_line,
            self.start_column,
            message,
        )
        self.diagnostics.append(diagnostic)