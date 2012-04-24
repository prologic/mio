#!/usr/bin/env python

from optparse import OptionParser
from signal import signal, SIGINT, SIG_IGN

import mio
from mio.interpreter import Interpreter

USAGE = "%prog [options] ... [-e expr | file | -]"
VERSION = "%prog v" + mio.__version__


def parse_options():
    parser = OptionParser(usage=USAGE, version=VERSION)

    parser.add_option("-e", "",
            action="store", default=None, dest="eval", metavar="expr",
            help="evalulate the given expression and exit")

    parser.add_option("-i", "",
            action="store_true", default=False, dest="interpreter",
            help="run the interpreter after processing the given files")

    parser.add_option("-d", "",
            action="store_true", default=False, dest="debug",
            help="enable debugging output")

    opts, args = parser.parse_args()

    return opts, args


def main():
    opts, args = parse_options()

    signal(SIGINT, SIG_IGN)

    interpreter = Interpreter(opts)

    if opts.eval:
        interpreter.eval(opts.eval)
    elif args:
        interpreter.load(args[0])
        if opts.interpreter:
            interpreter.repl()
    else:
        interpreter.repl()

if __name__ == "__main__":
    main()
