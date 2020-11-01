import sys
import os
from scanner import Scanner


class Interpreter:
    __slots__ = ('had_error')

    def __init__(self):
        self.had_error = False

    def run_file(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                self.run(f.read())
        else:
            print('File does not exist')

    def run(self, line):
        scanner = Scanner(line)
        tokens = scanner.scan_tokens()

        for token in tokens:
            print(token)

    def run_prompt(self):
        line = input('> ')
        while (len(line) > 0 and line != None and line != EOF):
            self.run(line)
            line = input('> ')

    def error(self, line, message):
        self.report_error(line, "", message)

    def report_error(self, line, where, message):
        print("[line " + line + "] Error" + where + ": " + message)
        self.had_error = True

if __name__ == '__main__':
    lox_interpreter = Interpreter()

    if len(sys.argv) > 2:
        print('Usage: python3 lox.py [script]')
    elif len(sys.argv) == 2:
        lox_interpreter.run_file(sys.argv[1])
        if lox_interpreter.had_error:
            sys.exit(65)
    else:
        lox_interpreter.run_prompt()
        lox_interpreter.had_error = False
