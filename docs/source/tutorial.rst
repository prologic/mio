mio Tutorial
============


Expressions
-----------


.. code-block:: mio
    
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
---------


.. code-block:: mio
    
    mio> a = 1
    ===> 1
    mio> a
    ===> 1
    mio> b = 2 * 3
    ===> 6
    mio> a + b
    ===> 7
    


Conditionals
------------


.. code-block:: mio
    
    mio> a = 2
    ===> 2
    mio> (a == 1) ifTrue(print("a is one")) ifFalse(print("a is not one"))
    a is not one
    


Lists
-----


.. code-block:: mio
    
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
---------


.. code-block:: mio
    
    mio> xs = [1, 2, 3]
    ===> [1, 2, 3]
    mio> xs foreach(x, print(x))
    1
    2
    3
    mio> it = iter(xs)
    ===> it(Object) at 0x155aae0:
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
-------


.. code-block:: mio
    
    mio> a = "foo"
    ===> u"foo"
    mio> b = "bar"
    ===> u"bar"
    mio> c = a + b
    ===> u"foobar"
    mio> c[0]
    ===> u'f'
    

.. code-block:: mio
    
    mio> s = "this is a test"
    ===> u"this is a test"
    mio> words = s split()
    ===> [u"this", u"is", u"a", u"test"]
    mio> s find("is")
    ===> 2
    mio> s find("test")
    ===> 10
    

Functions
---------


.. code-block:: mio
    
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
    

Objects
-------


.. code-block:: mio
    
    mio> World = Object clone()
    ===> World(Object) at 0x1416c18
    mio> World
    ===> World(Object) at 0x1416c18
    

Attributes
----------


.. code-block:: mio
    
    mio> World = Object clone()
    ===> World(Object) at 0xb24c18
    mio> World
    ===> World(Object) at 0xb24c18
    mio> World name = "World!"
    ===> u"World!"
    mio> World name
    ===> u"World!"
    

Methods
-------


.. code-block:: mio
    
    mio> World = Object clone()
    ===> World(Object) at 0xcdcc18
    mio> World
    ===> World(Object) at 0xcdcc18
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
    

