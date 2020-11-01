class Token:
    __slots__ = ('token_type', 'lexeme', 'literal', 'line')

    def __init__(self, token_type, lexeme, literal, line):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        return f"{self.token_type} {self.lexeme} {self.literal}"
