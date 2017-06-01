import operator

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
