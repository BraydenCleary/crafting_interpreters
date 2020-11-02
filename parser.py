from token_type import TokenType
from expression import Literal
from expression import Binary
from expression import Unary

class ParseError(Exception):
    pass

class Parser:
    def __init__(self, lox_env, tokens):
        self.lox_env = lox_env
        self.tokens = tokens
        self.current = 0

    def parse(self):
        try:
            return self.expression()
        except ParseError:
            return None

    def expression(self):
        return self.equality()

    def equality(self):
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(epr, operator, right)

        return expr

    def comparison(self):
        expr = self.term()

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self):
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self):
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self):
        if self.match(TokenType.FALSE):
            return Literal(False)
        elif self.match(TokenType.TRUE):
            return Literal(True)
        elif self.match(TokenType.NIL):
            return Literal(None)
        elif self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        elif self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression")
        else:
            self.error(self.peek(), "Expect expression")

    def consume(self, token_type, error_message):
        if self.check(token_type):
            return self.advance()

        raise self.error(self.peek(), message)

    def error(self, token, message):
        self.lox_env.error(token, message)
        raise ParseError()

    def synchronize(self):
        self.advance()

        # discard tokens until we find a statement boundary
        while not self.at_end():
            if self.previous().token_type == TokenType.SEMICOLON:
                return

            if self.peek().token_type in [TokenType.CLASS,
                                            TokenType.FUN,
                                            TokenType.VAR,
                                            TokenType.FOR,
                                            TokenType.IF,
                                            TokenType.WHILE,
                                            TokenType.PRINT,
                                            TokenType.RETURN]:
                return

            self.advance()

    def match(self, *token_types):
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True

        return False

    def check(self, token_type):
        if self.at_end():
            return False

        return self.peek().token_type == token_type;

    def advance(self):
        if not self.at_end():
            self.current += 1

        return self.previous()

    def previous(self):
        return self.tokens[self.current - 1]

    def peek(self):
        return self.tokens[self.current]

    def at_end(self):
        return self.peek().token_type == TokenType.EOF
