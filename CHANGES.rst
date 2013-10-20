Change Log
----------


mio 0.0.3
.........

- Improved test coverage
- Improved the ``Range`` object
- Fixed the scoping of ``block`` (s).
- Fixed the ``write`` and ``writeln`` methods of ``Object`` to not join arguments by a single space.
- Don't display ``None`` results in the REPL.
- Improved the ``__repr__`` of the ``File`` object.
- Added ``open`` and ``with`` builtins to the mio standard library.
- Implemented a basic import system in the mio standard library.


mio 0.0.2
.........

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


mio 0.0.1
.........

- Initial Release
