import sys
import os
from scanner import Scanner
from parser import Parser
from ast_printer import AstPrinter
from token_type import TokenType


class Lox:
    __slots__ = ('had_error')

    def __init__(self):
        self.had_error = False

    def error(self, token, message):
        if token.token_type == TokenType.EOF:
            self.report_error(token.line, " at end", message)
        else:
            self.report_error(token.line, f" at '{token.lexeme}'", message)

    def run_file(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                self.run(f.read())
        else:
            print('File does not exist')

    def run(self, line):
        scanner = Scanner(line)
        tokens = scanner.scan_tokens()
        parser = Parser(self, tokens)
        expression = parser.parse()

        if self.had_error:
            return

        print(AstPrinter().print(expression))

    def run_prompt(self):
        line = input('> ')
        while (len(line) > 0 and line != None and line != EOF):
            self.run(line)
            line = input('> ')

    def report_error(self, line, where, message):
        print(f"line {line} Error{where}: {message}")
        self.had_error = True

if __name__ == '__main__':
    lox = Lox()

    if len(sys.argv) > 2:
        print('Usage: python3 lox.py [script]')
    elif len(sys.argv) == 2:
        lox.run_file(sys.argv[1])
        if lox.had_error:
            sys.exit(65)
    else:
        lox.run_prompt()
        lox.had_error = False
