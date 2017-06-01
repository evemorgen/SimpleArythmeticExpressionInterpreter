import sys

from .constants import INTEGER, EOF
from .constants import sign_to_token, operators
from .token import Token


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
            self.get_next_token()
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
