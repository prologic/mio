============
mio Tutorial
============


Expressions
===========


.. runblock:: mio
    
    1 + 2
    1 + 2 * 3
    1 + (2 * 3)

.. note:: mio has no operator precedence (*in fact no operators*).
          You **must** use explicit grouping with parenthesis where
          appropriate in expressions.


Variables
=========


.. runblock:: mio
    
    a = 1
    a
    b = 2 * 3
    a + b


Conditionals
============


.. runblock:: mio
    
    a = 2
    (a == 1) ifTrue(print("a is one")) ifFalse(print("a is not one"))


Lists
=====


.. runblock:: mio
    
    xs = [30, 10, 5, 20]
    len(xs)
    print(xs)
    xs sort()
    xs[0]
    xs[-1]
    xs[2]
    xs remove(30)
    xs insert(1, 123)


Iteration
=========


.. runblock:: mio
    
    xs = [1, 2, 3]
    xs foreach(x, print(x))
    it = iter(xs)
    next(it)
    next(it)
    next(it)
    next(it)


Strings
=======


.. runblock:: mio
    
    a = "foo"
    b = "bar"
    c = a + b
    c[0]

.. runblock:: mio
    
    s = "this is a test"
    words = s split()
    s find("is")
    s find("test")


Functions
=========


.. runblock:: mio
    
    foo = block(
        print"foo"
    )
    foo()
    add = block(x, y,
        x + y
    )
    add(1, 2)

.. note:: Functions in mio do not have access to any outside state or globals
          (*there are no globals in mio*) with the only exception to the rule
          being closures.


Objects
=======


.. runblock:: mio
    
    World = Object clone()
    World


Attributes
----------


.. runblock:: mio
    
    World = Object clone()
    World
    World name = "World!"
    World name


Methods
-------


.. runblock:: mio
    
    World = Object clone()
    World
    World name = "World!"
    World name
    World hello = method(
        print("Hello", self name)
    )
    World hello()

.. note:: Methods implicitly get the receiving object as the first argument self passed.


Traits
======


.. runblock:: mio
    
    TGreetable = Object clone() do (
        hello = method(
            print("Hello", self name)
        )
    )
    World = Object clone() do (
        uses(TGreetable)
        
        name = "World!"
    )
    World
    World traits
    World behaviors
    World hello()
