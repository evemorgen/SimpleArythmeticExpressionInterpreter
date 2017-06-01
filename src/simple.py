import operator
import sys
import logging
import argparse

INTEGER = 'INTEGER'
PLUS = 'ADD'
MINUS = 'SUB'
MULTIPLY = 'MUL'
DIVIDE = 'DIV'
EOF = 'END'

operators = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

sign_to_token = {
    '+': PLUS,
    '-': MINUS,
    '*': MULTIPLY,
    '/': DIVIDE
}

FORMAT = '\033[1;31m[%(asctime)s]\033[32m[%(module)s/%(funcName)s/%(lineno)s]\033[1;0m %(message)s'

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )


class Interpreter(object):
    def __init__(self, text):
        self.text = text.replace(' ', '')  # skip all spaces
        self.pos = 0
        self.current_token = None

    def error(self):
        print('Unexpected token {0} at {1}'.format(self.current_token.type, self.pos - 1))
        sys.exit(-1)

    def get_next_token(self):
        text = self.text

        if self.pos > len(text) - 2:
            return Token(EOF, None)

        current_char = text[self.pos]
        if current_char.isdigit():
            start_pos = self.pos
            while current_char.isdigit() and self.pos < len(text) - 1:
                self.pos += 1
                current_char = text[self.pos]
            token = Token(INTEGER, int(text[start_pos:self.pos] if self.pos < len(text) - 1 else text[start_pos:]))
            #self.pos += 1
            return token

        if current_char in sign_to_token:
            token = Token(sign_to_token[current_char], current_char)
            self.pos += 1
            return token

        self.error()

    def eat(self, token_type):
        if isinstance(token_type, str):
            token_type = [token_type]
        if self.current_token.type in token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        result = None
        self.current_token = self.get_next_token()
        left = self.current_token
        if self.pos == len(self.text) - 1:
            eof = self.get_next_token()
            self.eat(INTEGER)
            return left.value

        self.eat(INTEGER)
        while self.pos < len(self.text) - 1:
            op = self.current_token
            self.eat(sign_to_token.values())
            right = self.current_token
            self.eat(INTEGER)
            result = operators[op.value](left.value, right.value)
            left.value = result
        if result is None:
            self.error()
        return result


def main():
    parser = argparse.ArgumentParser(description='Simple arithmetic expression interpreter')
    parser.add_argument('-v', '--verbose', help='verbose/debug mode', action='store_true')
    parser.add_argument('-e', '--execute', help='pass arythmetic expression inline', action='store', metavar='expr')
    args = parser.parse_args()
    if args.verbose is True:
        logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt="%H:%M:%S")
        logging.warning("running in debug mode")
    if args.execute is not None:
        logging.debug("taking inline expression")
        interpreter = Interpreter(args.execute)
        print(interpreter.expr())
        sys.exit(0)
    logging.debug("getting expression from stdin")
    for text in sys.stdin:
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(interpreter.expr())

if __name__ == '__main__':
    main()
