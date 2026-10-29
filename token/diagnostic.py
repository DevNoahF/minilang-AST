
class Diagnostic:
    def __init__(self, character, line, column, message):
        self.character = character
        self.line = line
        self.column = column
        self.message = message

    def __repr__(self):
        return (
            f"Diagnostic({self.character!r}, {self.line}:{self.column}, "
            f"{self.message!r})"
        )
        
def is_ascii_digit(c):
    return "0" <= c <= "9"


def is_ascii_letter(c):
    return ("a" <= c <= "z") or ("A" <= c <= "Z")


def is_identifier_start(c):
    return is_ascii_letter(c) or c == "_"


def is_identifier_part(c):
    return is_ascii_letter(c) or is_ascii_digit(c) or c == "_"


def is_whitespace(c):
    return c == " " or c == "\t" or c == "\r" or c == "\n"