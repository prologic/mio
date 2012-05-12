#!/usr/bin/env python

from glob import glob
from optparse import OptionParser
from signal import signal, SIGINT, SIG_IGN

import mio
from mio import runtime

USAGE = "%prog [options] ... [-e expr | file | -]"
VERSION = "%prog v" + mio.__version__


def parse_options():
    parser = OptionParser(usage=USAGE, version=VERSION)

    parser.add_option("-e", "",
            action="store", default=None, dest="eval", metavar="expr",
            help="evalulate the given expression and exit")

    parser.add_option("-i", "",
            action="store_true", default=False, dest="interactive",
            help="run interactively after processing the given files")

    parser.add_option("-d", "",
            action="store_true", default=False, dest="debug",
            help="enable debugging output")

    opts, args = parser.parse_args()

    return opts, args


def main():
    opts, args = parse_options()

    signal(SIGINT, SIG_IGN)

    runtime.init(opts)

    for filename in glob("./lib/*.mio"):
        runtime.state.load(filename)

    if opts.eval:
        runtime.state.eval(opts.eval)
    elif args:
        runtime.state.load(args[0])
        if opts.interactive:
            runtime.state.repl()
    else:
        runtime.state.repl()

if __name__ == "__main__":
    main()
