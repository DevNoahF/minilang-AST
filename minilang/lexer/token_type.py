class TokenType:
    KW_INT = "KW_INT"
    KW_BOOL = "KW_BOOL"
    KW_TRUE = "KW_TRUE"
    KW_FALSE = "KW_FALSE"
    KW_AND = "KW_AND"
    KW_OR = "KW_OR"
    KW_PRINT = "KW_PRINT"
    KW_IF = "KW_IF"
    KW_ELSE = "KW_ELSE"
    KW_WHILE = "KW_WHILE"
    KW_FOR = "KW_FOR"

    IDENT = "IDENT"
    INT_LITERAL = "INT_LITERAL"

    ASSIGN = "ASSIGN"
    PLUS = "PLUS"
    MINUS = "MINUS"
    STAR = "STAR"
    SLASH = "SLASH"

    EQUAL_EQUAL = "EQUAL_EQUAL"
    BANG_EQUAL = "BANG_EQUAL"
    LESS = "LESS"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER = "GREATER"
    GREATER_EQUAL = "GREATER_EQUAL"

    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    SEMICOLON = "SEMICOLON"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    EOF = "EOF"

KEYWORDS = {
    "int": TokenType.KW_INT,
    "bool": TokenType.KW_BOOL,
    "true": TokenType.KW_TRUE,
    "false": TokenType.KW_FALSE,
    "True": TokenType.KW_TRUE,
    "False": TokenType.KW_FALSE,
    "AND": TokenType.KW_AND,
    "OR": TokenType.KW_OR,
    "print": TokenType.KW_PRINT,
    "if": TokenType.KW_IF,
    "else": TokenType.KW_ELSE,
    "while": TokenType.KW_WHILE,
    "for": TokenType.KW_FOR,
}
