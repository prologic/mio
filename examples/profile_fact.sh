#!/bin/bash

python -m timeit -s "from mio import runtime; runtime.init(); runtime.state.load('fact.mio');" "runtime.state.eval('10 fact')"
