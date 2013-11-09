#!/bin/bash

echo -n "mio: "
python -m timeit -c -s "from mio import runtime; runtime.init(); runtime.state.eval('fact = block(n, reduce(block(a, x, a * x), 1..n))');" "runtime.state.eval('fact(10)')"

echo -n "python: "
python -m timeit -c -s "fact = lambda n: reduce(lambda a, x: a * x, range(1, n))" "fact(10)"
