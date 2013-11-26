#!/usr/bin/env python

"""mio interpreter for sphinxcontrib.autorun"""


import sys


from mio import runtime
from mio.main import parse_args


def main():
    """
    Print lines of input along with output.
    """

    opts, args = parse_args(sys.argv)
    runtime.init(args, opts)
    console = runtime.state

    source_lines = (line.rstrip() for line in sys.stdin)
    source = ""
    try:
        while True:
            source = source_lines.next()
            print "mio>", source
            more = console.runsource(source)
            while more:
                next_line = source_lines.next()
                print "....", next_line
                source += "\n" + next_line
                more = console.runsource(source)
    except StopIteration:
        if more:
            print ".... "
            more = console.runsource(source + "\n")


if __name__ == "__main__":
    main()
