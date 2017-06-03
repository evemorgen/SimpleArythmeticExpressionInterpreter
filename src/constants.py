import operator

INTEGER = 'INTEGER'
PLUS = 'ADD'
MINUS = 'SUB'
MULTIPLY = 'MUL'
DIVIDE = 'DIV'
LEFT_BRACKET = 'OPENING_BRACKET'
RIGHT_BRACKET = 'CLOSING_BRACKET'
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

tokens = {v: k for k, v in sign_to_token.items()}

brackets = {
    '(': LEFT_BRACKET,
    ')': RIGHT_BRACKET
}

FORMAT = '\033[1;31m[%(asctime)s]\033[32m[%(module)s/%(funcName)s/%(lineno)s]\033[1;0m %(message)s'
