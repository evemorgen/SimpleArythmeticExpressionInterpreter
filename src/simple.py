import sys
import logging
import argparse

from constants import FORMAT
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
        interpreter = Interpreter(args.execute)
        print(interpreter.expr())
    else:
        logging.debug("no arguments provided, getting expression from stdin")
        for text in sys.stdin:
            interpreter = Interpreter(text)
            print(interpreter.get_multidigit_integer(0))


if __name__ == '__main__':
    main()
