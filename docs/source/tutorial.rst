============
mio Tutorial
============


Expressions
===========


::
    
    mio> 1 + 2
    ===> 3
    mio> 1 + 2 * 3
    ===> 9
    mio> 1 + (2 * 3)
    ===> 7
    

.. note:: mio has no operator precedence (*in fact no operators*).
          You **must** use explicit grouping with parenthesis where
          appropriate in expressions.


Variables
=========


::
    
    mio> a = 1
    ===> 1
    mio> a
    ===> 1
    mio> b = 2 * 3
    ===> 6
    mio> a + b
    ===> 7
    


Conditionals
============


::
    
    mio> a = 2
    ===> 2
    mio> (a == 1) ifTrue(print("a is one")) ifFalse(print("a is not one"))
    a is not one
    


Lists
=====


::
    
    mio> xs = [30, 10, 5, 20]
    ===> [30, 10, 5, 20]
    mio> len(xs)
    ===> 4
    mio> print(xs)
    [30, 10, 5, 20]
    mio> xs sort()
    ===> [5, 10, 20, 30]
    mio> xs[0]
    ===> 5
    mio> xs[-1]
    ===> 30
    mio> xs[2]
    ===> 20
    mio> xs remove(30)
    ===> [5, 10, 20]
    mio> xs insert(1, 123)
    ===> [5, 123, 10, 20]
    


Iteration
=========


::
    
    mio> xs = [1, 2, 3]
    ===> [1, 2, 3]
    mio> xs foreach(x, print(x))
    1
    2
    3
    mio> it = iter(xs)
    ===> it(Object) at 0x1c83b48:
      N               = 2
      i               = -1
      iterable        = [1, 2, 3]
    mio> next(it)
    ===> 1
    mio> next(it)
    ===> 2
    mio> next(it)
    ===> 3
    mio> next(it)
    ===> 'UserError'
    


Strings
=======


::
    
    mio> a = "foo"
    ===> u"foo"
    mio> b = "bar"
    ===> u"bar"
    mio> c = a + b
    ===> u"foobar"
    mio> c[0]
    ===> u'f'
    

::
    
    mio> s = "this is a test"
    ===> u"this is a test"
    mio> words = s split()
    ===> [u"this", u"is", u"a", u"test"]
    mio> s find("is")
    ===> 2
    mio> s find("test")
    ===> 10
    


Functions
=========


::
    
    mio> foo = block(print"foo")
    ===> block():
      args            = args()
      body            = body()
      kwargs          = kwargs()
    mio> foo()
    ===> u"foo"
    mio> add = block(x, y, x + y)
    ===> block(x, y):
      args            = args()
      body            = body()
      kwargs          = kwargs()
    mio> add(1, 2)
    ===> 3
    

.. note:: Functions in mio do not have access to any outside state or globals (*there are no globals in mio*)
          with the only exception to the rule being closures.


Objects
=======


::
    
    mio> World = Object clone()
    ===> World(Object) at 0x1449c80
    mio> World
    ===> World(Object) at 0x1449c80
    


Attributes
----------


::
    
    mio> World = Object clone()
    ===> World(Object) at 0x260cc80
    mio> World
    ===> World(Object) at 0x260cc80
    mio> World name = "World!"
    ===> u"World!"
    mio> World name
    ===> u"World!"
    


Methods
-------


::
    
    mio> World = Object clone()
    ===> World(Object) at 0x1daec80
    mio> World
    ===> World(Object) at 0x1daec80
    mio> World name = "World!"
    ===> u"World!"
    mio> World name
    ===> u"World!"
    mio> World hello = method(print("Hello", self name))
    ===> method():
      args            = args()
      body            = body()
      kwargs          = kwargs()
    mio> World hello()
    Hello World!
    

.. note:: Methods implicitly get the receiving object as the first argument self passed.


Traits
======


::
    
    mio> TGreetable = Object clone() do ( hello = method(print("Hello", self name)) )
    ===> TGreetable(Object) at 0x2302ce8:
      hello           = method()
    mio> World = Object clone() do ( uses(TGreetable); name = "World!" )
    ===> World(Object) at 0x2302e20:
      name            = u"World!"
    mio> World
    ===> World(Object) at 0x2302e20:
      name            = u"World!"
    mio> World traits
    ===> [TGreetable(Object) at 0x2302ce8]
    mio> World behaviors
    ===> ['hello']
    mio> World hello()
    Hello World!
    
