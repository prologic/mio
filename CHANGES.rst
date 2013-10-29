Changes
-------


mio 0.0.5.dev
.............

- Split up core into core and types.
- Re-implemented ``True``, ``False`` and ``None`` in mio.
- Implemented ``bin`` builtin.
- Implemented ``bool`` builtin.
- Implemented ``callable`` builtin.
- Implemented ``cha`` builtin.
- IMplemented ``from`` and ``import`` builtins.


mio 0.0.4 (*2013-10-27*)
........................

- Moved the implementation of ``super`` to the mio std. lib
- Only set ``_`` as the last result in the Root object (*the Lobby*)
- Added support for ``()``, ``[]`` and ``{}`` special messages that can be used to define syntactic suguar for lists, dicts, etc.
- Implemented ``Dict`` object type and ``{a=1, b=2}`` syntactic sugar to the builtint (*mio std. lib*) ``dict()`` method.
- Refactored the ``File`` object implementation and made it's repr more consistent with other objects in mio.
- Fixed keyword argument support.
- Fixed a few minor bugs in the ``Message`` object and improved test coverage.
- Added ``?`` as a valid operator and an implementation of ``Object ?message`` in the mio std. lib.
- Fixed a bug with ``Range``'s internal iterator causing ``Range asList`` not to work.
- Fixed a bug with ``Object foreach`` and ``continue``.
- **Achived 100% test coverage!**
- Implemented ``*args`` and ``**kwargs`` support for methods and blocks.
- Removed ``Object`` methods ``print``, ``println``, ``write`` and ``writeln`` in favor of the new builtin ``print`` function in the mio std. lib
- Added an implemenation of ``map`` to the mio std. lib
- Fixed a bug with the parser where an argument's previous attribute was not getting set correctly.
- Reimplemented ``not`` in the mio std. lib and added ``-=``, ``*=`` and ``/=`` operators.
- Added a ``Object :foo`` (*primitive*) method using the ``:`` operator. This allows us to dig into the host object's internal methods.
- Added an implementation of ``abs`` builtin using the primitive method.
- Changed the ``import`` function to return the imported module (*instead of ``None``*) so you can bind imported modules to explicitly bound names.
- Added ``from`` an alias to ``import`` and ``Module import`` so you can do:

::
    
    bar = from(foo) import(bar)
    
- Fixed some minor bugs in ``Object foreach`` and ``Object while`` where a ReturnState was not passed up to the callee.
- Added implementations of ``all`` and ``any`` to the mio std. lib.
- Added this.mio (The Zen of mio ala Zen of Python)
- Added List insert method and internal __len__.
- Moved the implementations of the ``Importer`` and ``Module`` objects to the host language (*Python*).
- Added support for modifying the ``Importer`` search path.
- Restructured the mio std. library and moved all bootstrap modules into ./lib/bootstrap
- Added (almost) Python-style string literal support. Triple Quote, Double, Quote, Single Quote, Short and Long Strings
- Added support for exponents with number literals.
- Added internal ``tomio`` and ``frommio`` type converion function.
- Added an ``FFI`` implementation that hooks directly into the host language (*Python*).
- Implemented the ``antigravity`` module in mio.
- Added support for exposing builtin functions as well in the FFI.
- Simplified the two examples used in the docs and readme and write a simple bash script to profile the factorial example.
- Changed the calling semantics so that calls to methods/blocks are explicitly made with ``()``.
- Added a new internal attribute to ``Object`` called ``binding`` used to show the binding of a bound object in repr(s).


mio 0.0.3 (*2013-10-20*)
........................

- Improved test coverage
- Improved the ``Range`` object
- Fixed the scoping of ``block`` (s).
- Fixed the ``write`` and ``writeln`` methods of ``Object`` to not join arguments by a single space.
- Don't display ``None`` results in the REPL.
- Improved the ``__repr__`` of the ``File`` object.
- Added ``open`` and ``with`` builtins to the mio standard library.
- Implemented a basic import system in the mio standard library.
- Implemented ``Dict items`` method.


mio 0.0.2 (*2013-10-19*)
........................

- Include lib as package data
- Allow mio modules to be loaded from anywhere so mio can be more usefully run from anywhere
- Added bool type converion
- Improved the documentation and added docs for the grammar
- Changed Lobby object to be called Root
- Added an -S option (don't load system libraries).
- Added unit test around testing for last value with return
- Refactored Message.eval to be non-recursive
- Set _ in the context as the last valeu
- Implemented Blocks and Methods
- Fixed return/state issue by implementing Object evalArg and Object evalArgAndReturnSelf in Python (not sure why this doesn't work in mio itself)
- Implemented Object evalArgAndReturnNone


mio 0.0.1 (*2013-10-19*)
........................

- Initial Release
