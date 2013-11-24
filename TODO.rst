TODO
====

- Fix user errors.
- Implement ``__slice__``, ``slice(...)`` and ``xs[start:[end][:step]``

- Change the way we construct user objects.

  - Pretty sure we can just create new instances rather than ``runtime.find(...).clone(...)``

- Change the way methods and blocks are bound and unifiy them into a single entity.

  - Unified method: ``method(...)``.
  - Can be dynamically bound to objects.
  - Is always passed it's bound object as the first parameter ``self``.
  - Are by default bound to the context they are created in.

- Fix keyword argument(s) parameters.
- Bring test coverage back up to 100%
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
