from lox_error import LoxError
from lox_token import Token
from token_type import TokenType
from token_type import KEYWORD_TOKENS
from token_type import ONE_CHARACTER_TOKENS
from token_type import ONE_OR_MANY_CHARACTER_TOKENS

WHITESPACE_CHARACTERS = set({' ', '\r', '\t'})

NEWLINE_CHARACTER = '\n'

class Scanner:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self):
        while (self.more_to_scan()):
            self.start = self.current;
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, '', None, self.line))
        return self.tokens

    def scan_token(self):
        character = self.advance()

        if character in ONE_CHARACTER_TOKENS.keys():
            self.add_token(ONE_CHARACTER_TOKENS[character])
        elif character in ONE_OR_MANY_CHARACTER_TOKENS.keys():
            if character == '!':
                self.add_token(TokenType.BANG_EQUAL if self.advance_if_match('=') else TokenType.BANG)
            elif character == '=':
                self.add_token(TokenType.EQUAL_EQUAL if self.advance_if_match('=') else TokenType.EQUAL)
            elif character == '<':
                self.add_token(TokenType.LESS_EQUAL if self.advance_if_match('=') else TokenType.LESS)
            elif character == '>':
                self.add_token(TokenType.GREATER_EQUAL if self.advance_if_match('=') else TokenType.GREATER)
            elif character == '/':
                # we know we're scanning a comment
                if self.advance_if_match('/'):
                    # so we're gonna ignore all characters until we see a newline
                    while self.more_to_scan() and self.peek(1) != '\n':
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
        elif character in WHITESPACE_CHARACTERS:
            return
        elif character in NEWLINE_CHARACTER:
            self.line += 1
        elif character == '"':
            self.handle_string()
        elif character.isdigit():
            self.handle_number()
        elif character.isalpha():
            self.handle_identifier()
        else:
            raise LoxError(self.line, 'Unexpected character')

    def handle_identifier(self):
        while (self.peek(1).isalpha() or self.peek(1) == '_' or self.peek(1).isdigit()):
            self.advance()

        text = self.source[self.start:self.current]

        token_type = KEYWORD_TOKENS[text]

        if token_type:
            self.add_token(token_type)
        else:
            self.add_token(TokenType.IDENTIFIER)

    def handle_number(self):
        while self.peek(1).isdigit():
            self.advance()

        if self.peek(1) == '.' and self.peek(2).isdigit():
            self.advance()

            while self.peek(1).isdigit():
                self.advance()

        self.add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))

    def handle_string(self):
        while self.peek(1) != '"' and self.more_to_scan():
            if self.peek(1) == '\n':
                self.line += 1
            self.advance()

        self.advance()

        if not self.more_to_scan():
            raise LoxError(self.line, "Unterminated string")
            return

        literal = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, literal)

    def advance_if_match(self, expected):
        if not self.more_to_scan() or self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self, lookahead):
        if lookahead > 2:
            raise LoxError(self.line, "Trying to look too many characters ahead")

        if not self.current - 1 + lookahead < len(self.source):
            return None

        return self.source[self.current - 1 + lookahead]

    def add_token(self, token_type, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def more_to_scan(self):
        return self.current < len(self.source)
