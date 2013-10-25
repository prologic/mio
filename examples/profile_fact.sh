#!/bin/bash

echo -n "mio: "
python -m timeit -s "from mio import runtime; runtime.init(); runtime.state.load('fact.mio');" "runtime.state.eval('10 fact')"

echo -n "python: "
python -m timeit -s "fact = lambda x: 1 if x == 0 else x * fact(x-1)" "fact(10)"
