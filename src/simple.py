import sys
import logging
import argparse

from constants import FORMAT, EOF
from interpreter import Interpreter


def main():
    parser = argparse.ArgumentParser(description='Simple arithmetic expression interpreter')
    parser.add_argument('-v', '--verbose', help='verbose/debug mode', action='store_true')
    parser.add_argument('-e', '--execute', help='pass arythmetic expression inline', action='store', metavar='expr')
    args = parser.parse_args()

    if args.verbose is True:
        logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt="%H:%M:%S")
        logging.warning("-v provided, running in debug mode")

    if args.execute is not None:
        logging.debug("-e provided, taking inline expression")
        text = args.execute
    else:
        logging.debug("no arguments provided, getting expression from stdin")
        text = next(sys.stdin)

    interpreter = Interpreter(text)
    res = int(interpreter.expr())
    if interpreter.current_token.type != EOF:
        interpreter.error(interpreter.current_token, interpreter.current_token_number)
    print(res)


if __name__ == '__main__':
    main()
