"""Pacote da MiniLang: analisador léxico manual."""

from .lexer import Lexer, Token, TokenType, Diagnostic

__all__ = ["Lexer", "Token", "TokenType", "Diagnostic"]
