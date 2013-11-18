mio Tutorial
============


Expressions
-----------


.. program-output:: mio -v -e "1 + 2" -e "1 + 2 * 3" -e "(1 + 2) * 3"

.. note:: mio has no operator precedence (*in fact no operators*).
          You **must** use explicit grouping with parenthesis where
          appropriate in expressions.


Variables
---------


.. program-output:: mio -v -e "a = 1" -e "a" -e "b = 2 * 3" -e "a + b"


Conditionals
------------


.. program-output:: mio -v -e "a = 2" -e "(a == 1) ifTrue(print(\"a is one\")) ifFalse(print(\"a is not one\"))"


Lists
-----


.. program-output:: mio -v -e "xs = [30, 10, 5, 20]" -e "len(xs)" -e "print(xs)" -e "xs sort()" -e "xs[0]" -e "xs[-1]" -e "xs[2]" -e "xs remove(30)" -e "xs insert(1, 123")


Iteration
---------


.. program-output:: mio -v -e "xs = [1, 2, 3]" -e "xs foreach(x, print(x))" -e "it = iter(xs)" -e "next(it)" -e "next(it)" -e "next(it)" -e "next(it)"


Strings
-------


.. program-output:: mio -v -e "a = \"foo\"" -e "b = \"bar\"" -e "c = a + b" -e "c[0]"

.. program-output:: mio -v -e "s = \"this is a test\"" -e "words = s split()" -e "s find(\"is\")" -e "s find(\"test\")"
