Grammar
=======


The following EBNF Grammar defines the Syntax for mio:

.. productionlist::
   operator   : "**" | "++" | "--" | "+=" | "-=" | "*=" | "/=" | "<<" | ">>" |
              : "==" | "!=" | "<=" | ">=" | "+"  | "-"  | "*"  | "/"  | "="  |
              : "<"  | ">"  | "!"  | "%"  | "|"  | "^"  | "&"  | "is" | "or" |
              : "and" |  "not" |
              : "return"
   comment    : r"^#.*$"
   whitespace : r"[ \t]+"
   string     : r'"[^"]*"'
   number     : r'-?([0-9]+(\.[0-9]*)?)'
   identifier : r'[A-Za-z_][A-Za-z0-9_]*'
   terminator : ";" | "\r" | "\n"
   expression : (message | terminator)*
   message    : (symbol, [ arguments ]) | arguments
   opening    : "(" | "{" | "["
   closing    : ")" | "}" | "]"
   arguments  : opening , ( expression, ( "," , expression )* )* , closing
   symbol     : identifier | number | operator | string
