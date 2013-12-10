TODO
====

- Update the ``docs/source/grammar.rst`` and try to auto-generate it from the parser via ``.ebnf()``
- Fix ``property.mio`` example and basic data descriptors.
- Fix ``Object super()``. Make it a builtin.
- Deal with this better and raise a better error instead of crashing.

::
    
    x = method(1 + 1, a, b,
        a + b
    )
    
- Implement ``__slice__``, ``slice(...)`` and ``xs[start:[end][:step]``

- Change the way methods and blocks are bound and unifiy them into a single entity.

  - Unified method: ``method(...)``.
  - Can be dynamically bound to objects.
  - Is always passed it's bound object as the first parameter ``self``.
  - Are by default bound to the context they are created in.

- Fix keyword argument(s) parameters.
- Figure out a way to avoid recursion so ``loop(print("foo"))`` works as expected.
- Write a testing framework for mio in mio.
- Implement a "trace" hook into the interpreter. i.e: Python's ``sys.settrace()``
- Implement a basic debugger.
- Implement a basic coverage tool.
- Add ``__doc__`` (*doc strings*) support.
- Implement a basic help system.
- Do a refresher on how to write an interpreter in RPython and write a really really simple one:

  - http://doc.pypy.org/en/latest/coding-guide.html#restricted-python
  - http://morepypy.blogspot.com.au/2011/04/tutorial-writing-interpreter-with-pypy.html
