#!/bin/bash

cat <<EOF
mio Tutorial
============


Expressions
-----------


EOF
echo ".. code-block:: mio"
echo "    "
mio -v -e "1 + 2" -e "1 + 2 * 3" -e "1 + (2 * 3)" | sed -e "s/^/    /"
echo "    "
echo
cat <<EOF
.. note:: mio has no operator precedence (*in fact no operators*).
          You **must** use explicit grouping with parenthesis where
          appropriate in expressions.


Variables
---------


EOF
echo ".. code-block:: mio"
echo "    "
mio -v -e "a = 1" -e "a" -e "b = 2 * 3" -e "a + b" | sed -e "s/^/    /"
echo "    "
echo
cat <<EOF

Conditionals
------------


EOF
echo ".. code-block:: mio"
echo "    "
mio -v -e "a = 2" -e "(a == 1) ifTrue(print(\"a is one\")) ifFalse(print(\"a is not one\"))" | sed -e "s/^/    /"
echo "    "
echo
cat <<EOF

Lists
-----


EOF
echo ".. code-block:: mio"
echo "    "
mio -v -e "xs = [30, 10, 5, 20]" -e "len(xs)" -e "print(xs)" -e "xs sort()" -e "xs[0]" -e "xs[-1]" -e "xs[2]" -e "xs remove(30)" -e "xs insert(1, 123)" | sed -e "s/^/    /"
echo "    "
echo
cat <<EOF

Iteration
---------


EOF
echo ".. code-block:: mio"
echo "    "
mio -v -e "xs = [1, 2, 3]" -e "xs foreach(x, print(x))" -e "it = iter(xs)" -e "next(it)" -e "next(it)" -e "next(it)" -e "next(it)" | sed -e "s/^/    /"
echo "    "
echo
cat <<EOF

Strings
-------


EOF
echo ".. code-block:: mio"
echo "    "
mio -v -e "a = \"foo\"" -e "b = \"bar\"" -e "c = a + b" -e "c[0]" | sed -e "s/^/    /"
echo "    "
echo
echo ".. code-block:: mio"
echo "    "
mio -v -e "s = \"this is a test\"" -e "words = s split()" -e "s find(\"is\")" -e "s find(\"test\")" | sed -e "s/^/    /"
echo "    "
echo
cat <<EOF
Functions
---------


EOF
echo ".. code-block:: mio"
echo "    "
mio -v -e "foo = block(print\"foo\")" -e "foo()" -e "add = block(x, y, x + y)" -e "add(1, 2)" | sed -e "s/^/    /"
echo "    "
echo
cat <<EOF
Objects
-------


EOF
echo ".. code-block:: mio"
echo "    "
mio -v -e "World = Object clone()" -e "World" | sed -e "s/^/    /"
echo "    "
echo
cat <<EOF
Attributes
----------


EOF
echo ".. code-block:: mio"
echo "    "
mio -v -e "World = Object clone()" -e "World" -e "World name = \"World!\"" -e "World name" | sed -e "s/^/    /"
echo "    "
echo
cat <<EOF
Methods
-------


EOF
echo ".. code-block:: mio"
echo "    "
mio -v -e "World = Object clone()" -e "World" -e "World name = \"World!\"" -e "World name" -e "World hello = method(print(\"Hello\", self name))" -e "World hello()" | sed -e "s/^/    /"
echo "    "
echo
