# Target:   test
# Date:     11th November 2013
# Author:   James Mills, prologic at shortcircuit dot net dot au

"""RPython Entry Point: test"""


try:
    from rpython.rlib.streamio import open_file_as_stream
except ImportError:
    open_file_as_stream = open


def input(prompt=None):
    search = "\n"
    stdin = open_file_as_stream("/dev/stdin", "r", 1024)
    stdout = open_file_as_stream("/dev/stdout", "w", 1024)
    if prompt is not None:
        stdout.write(prompt)
        stdout.flush()
    while True:
        try:
            line = stdin.readline()
        except (KeyboardInterrupt, EOFError):
            return

        if not line:
            return
        if search in line:
            return line


def main(argv):
    print("Hello World!")
    name = input("What is your name? ")
    if name is not None:
        print("Hello " + name)
    return 0


def target(*args):
    return main, None


if __name__ == "__main__":
    import sys
    main(sys.argv)
