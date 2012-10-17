# -*- coding: utf-8 -*-

import string

import runtime
from object import Object
from message import Message
from utils import pymethod, Null


operators = [
    "**", "++", "--", "+=", "-=", "*=", "/=", "<<", ">>",
    "==", "!=", "<=", ">=",
    "+", "-", "*", "/", "=", "<", ">", "!", "%", "|", "^", "&",
    "is", "or", "and", "not", "return",
]


def is_op(s):
    return s in operators


def isspace(aCharacter):
    return aCharacter in string.whitespace


def isalpha(aCharacter):
    return (aCharacter in string.letters) or (aCharacter == '_')


def isIdentifier(aCharacter):
    return isalpha(aCharacter) or isdigit(aCharacter) or (aCharacter == '?')


def isdigit(aCharacter):
    return aCharacter in string.digits


endOfInput = -1


class Lexer(object):
    """Lexes an input string for parsable symbols.

    Implements a single token look-ahead.

    Fields:
        current = the current, or pending, symbol in the source text to be
                  consumed by a parser.  Will be set to endOfInput when there
                  is no more input data to lex.  Strings will include their
                  leading quotes.

        next = the next after current symbol in the input stream.
    """

    def __init__(self, string):
        self.input = string
        self.current = None
        self.next = None
        self.pump()
        self.pump()

    def pump(self):
        """Consumes a single lexical token.  What was in next
        now appears in current, and a new value is loaded into
        next.
        """

        self.current = self.next
        self.lex()

    def pendingCharacter(self):
        return self.input[0]

    def advanceCharacter(self):
        self.input = self.input[1:]

    def parseIdentifier(self):
        largestIndex = len(self.input)
        i = 0
        while (i < largestIndex) and isIdentifier(self.input[i]):
            i = i + 1

        self.next = self.input[0:i]
        self.input = self.input[i:]

    def parseNumber(self):
        largestIndex = len(self.input)
        i = 0
        while (i < largestIndex) and isdigit(self.input[i]):
            i = i + 1

        self.next = self.input[0:i]
        self.input = self.input[i:]

    def parseQuotedString(self):
        largestIndex = len(self.input)
        i = 1   # index 0 is known to be a quote.
        while (i < largestIndex) and (self.input[i] != '"'):
            i = i + 1

        self.next = self.input[0:(i + 1)]
        self.input = self.input[(i + 1):]

    def lex(self):
        if self.input == "":
            self.next = endOfInput

        elif self.pendingCharacter() == '\n':
            self.next = ";"
            self.advanceCharacter()

        elif isspace(self.pendingCharacter()):
            self.advanceCharacter()
            self.lex()

        elif isalpha(self.pendingCharacter()):
            self.parseIdentifier()

        elif isdigit(self.pendingCharacter()):
            self.parseNumber()

        elif self.pendingCharacter() == '"':
            self.parseQuotedString()

        else:
            self.next = self.pendingCharacter()
            self.advanceCharacter()


def parseArguments(theLexer):
    args = []
    arg = []

    while theLexer.current != endOfInput:
        if theLexer.current == ')':
            if arg:
                args.append(arg)
            break

        elif theLexer.current == ',':
            args.append(arg)
            arg = []
            theLexer.pump()

        else:
            arg = parseExpression(theLexer)

    return args


def make_chain(messages):
    print "make_chain:", repr(messages)
    if messages == []:
        return Message("")

    key, value = None, None
    root, prev = None, None

    while True:
        if len(messages) > 1 and messages[1].name == "=":
            key = messages.pop(0)
            key = Message(key.name,
                    value=runtime.find("String").clone(key.name))
            op = messages.pop(0)
            if op.args:
                value = Message("", *op.args)
            else:
                value = messages.pop(0)

            message = Message("set", key, value)

            if root is None:
                root = prev = message
            else:
                prev.next = prev = message
        elif value is not None:
            if messages and not messages[0].terminator:
                if is_op(messages[0].name):
                    op = messages.pop(0)
                    if messages:
                        message = messages.pop(0)
                        op.args = (message,)
                    value.next = op
                    value = op
                else:
                    message = messages.pop(0)
                    value.next = message
                    value = message
            else:
                key, value = None, None
        elif messages and is_op(messages[0].name) and not messages[0].args:
            message = messages.pop(0)
            if root is None:
                root = prev = message
            else:
                prev.next = prev = message
            if messages:
                message = messages.pop(0)
                prev.args = message,
        elif messages:
            message = messages.pop(0)
            if root is None:
                root = prev = message
            else:
                prev.next = prev = message
        else:
            break

    print " root:", root
    return root


def parseExpression(theLexer):
    tree = []

    while theLexer.current != endOfInput:
        if theLexer.current == ",":
            break

        elif theLexer.current == ")":
            break

        elif theLexer.current == "(":
            theLexer.pump()
            args = parseArguments(theLexer)
            if theLexer.current == ")":
                if not tree:
                    tree = [Message("")]

                if tree[-1].args:
                    tree.append(Message(""))

                tree[-1].args = args
                theLexer.pump()
            else:
                print "Syntax Error: ')' expected"

        else:
            tree.append(Message(theLexer.current))
            theLexer.pump()

    return make_chain(tree)
    #return tree


def parse(aString):
    l = Lexer(aString)
    return parseExpression(l)


class Parser(Object):

    def __init__(self, value=Null):
        super(Parser, self).__init__(value=value)

        self.create_methods()
        self.parent = runtime.state.find("Object")

    @pymethod()
    def parse(self, receiver, context, m, code):
        code = str(code.eval(context))
        return parse(tokenize(code))
