import sys
import logging
import pprint
import copy

from constants import PLUS, MINUS, MULTIPLY, DIVIDE, INTEGER, EOF, LEFT_BRACKET, RIGHT_BRACKET
from constants import sign_to_token, operators, brackets, tokens
from my_token import Token


class Interpreter(object):

    def __init__(self, text):
        self.text = text.replace(' ', '')
        logging.debug("trimming spaces from string, before: '%s', after: '%s'", text, self.text)
        self.token_list = []
        self.find_tokens()
        self.current_token = self.token_list[0]
        self.current_token_number = 0

    def error(self, token, pos):
        print('Unexpected token {0} at {1}'.format(token, pos))
        sys.exit(-1)

    def get_multidigit_integer(self, start_pos):
        logging.debug("trying to match multidigit integer from position %s", start_pos)
        end_pos = start_pos
        while self.text[end_pos].isdigit() and end_pos < len(self.text) - 1:
            end_pos += 1
        if end_pos == len(self.text) - 1 and self.text[end_pos].isdigit():
            logging.debug("found %s at text[%s:], at the end of text", self.text[start_pos:], start_pos)
            return (self.text[start_pos:], end_pos + 1)
        else:
            logging.debug("found %s at text[%s:%s]", self.text[start_pos:end_pos], start_pos, end_pos)
            return (self.text[start_pos:end_pos], end_pos)

    def find_tokens(self):
        current_pos = 0
        while current_pos < len(self.text):
            if self.text[current_pos].isdigit() is True:
                logging.debug("found first digit of a integer, trying to parse whole of it")
                value, current_pos = self.get_multidigit_integer(current_pos)
                self.token_list.append(Token(INTEGER, int(value)))
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
        logging.debug("all tokens found:\n %s", pprint.pformat(self.token_list))

    def get_current_token(self):
        self.current_token_number += 1
        token = self.token_list[self.current_token_number]
        return token

    def eat(self, token_type):
        if isinstance(token_type, str):
            token_type = [token_type]
        logging.debug("trying to eat one of these: %s", token_type)
        if self.current_token.type in token_type:
            logging.debug("matching token found, getting next one")
            self.current_token = self.get_current_token()
        else:
            logging.debug("oops, bad token type found, panics all over")
            self.error(self.current_token, self.current_token_number)

    def factor(self):
        """factor : INTEGER | LEFT_BRACKET expr RIGHT_BRACKET"""
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            logging.debug("factor eated an integer: %s, proceeding", token)
            return token.value
        elif token.type == LEFT_BRACKET:
            self.eat(LEFT_BRACKET)
            result = self.expr()
            self.eat(RIGHT_BRACKET)
            return result

    def template(self, function, token_list):
        logging.debug("trying to run **%s** function", function.__name__)
        result = function()

        while self.current_token.type in token_list:
            token = self.current_token
            self.eat(token_list)
            result = operators[tokens[token.type]](result, function())
            logging.debug("calculating **%s**, partial result is: %s", function.__name__, result)
        return result

    def term(self):
        """term : factor ((MULTIPLY | DIVIDE) factor)*"""
        return self.template(self.factor, [MULTIPLY, DIVIDE])

    def expr(self):
        """expr   : term ((PLUS | MINUS) term)*"""
        return self.template(self.term, [PLUS, MINUS])
