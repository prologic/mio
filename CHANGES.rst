Changes
-------


mio 0.0.4.dev
.............

- Moved the implementation of ``super`` to the mio std. lib
- Only set ``_`` as the last result in the Root object (*the Lobby*)
- Chnaged the semantics of ``type`` such that ``type`` is bound to the name of the binding object.
- Improved test coverage
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
