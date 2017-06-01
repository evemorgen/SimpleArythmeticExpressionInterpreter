import sys
import logging

from constants import INTEGER, EOF
from constants import sign_to_token, operators, brackets
from my_token import Token


class Interpreter(object):

    def __init__(self, text):
        self.text = text.replace(' ', '')  # skip all spaces
        logging.debug("trimming spaces from string, before: '%s', after: '%s'", text, self.text)
        self.token_list = []
        self.current_token = None
        self.current_token_number = 0

    def error(self, token, pos):
        print('Unexpected token {0} at {1}'.format(token, pos))
        sys.exit(-1)

    def get_multidigit_integer(self, start_pos):
        logging.debug("trying to match multidigit integer from position %s", start_pos)
        end_pos = start_pos
        while self.text[end_pos].isdigit() and end_pos < len(self.text) - 1:
            end_pos += 1
        if end_pos == len(self.text) - 1:
            logging.debug("found %s at text[%s:], at the end of text", self.text[start_pos:], start_pos)
            return (self.text[start_pos:], end_pos)
        else:
            logging.debug("found %s at text[%s:%s]", self.text[start_pos:end_pos], start_pos, end_pos)
            return (self.text[start_pos:end_pos], end_pos)

    def find_tokens(self):
        current_pos = 0
        while current_pos < len(self.text) - 1:
            if self.text[current_pos].isdigit() is True:
                logging.debug("found first digit of a integer, trying to pare whole of it")
                value, current_pos = self.get_multidigit_integer(current_pos)
                self.token_list.append(Token(INTEGER, value))
            elif self.text[current_pos] in operators:
                logging.debug("found operator '%s', creating token", self.text[current_pos])
                operator_token = sign_to_token[self.text[current_pos]]
                self.token_list.append(Token(operator_token, None))
                current_pos += 1
            elif self.text[current_pos] in brackets:
                logging.debug("found bracket '%s', creating token", self.text[current_pos])
                bracket = brackets[self.text[current_pos]]
                self.token_list.append(Token(bracket, None))
                current_pos += 1
            else:
                logging.debug("something terribly wrong happend, cannot match this character: %s", self.text[current_pos])
                self.error("'{}'".format(self.text[current_pos]), current_pos)

        logging.debug("parsed whole string, adding EOF to token list")
        self.token_list.append(Token(EOF, None))

    def get_current_token(self):
        token = self.token_list[self.current_token_number]
        self.current_token_number += 1
        return token

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
