from parser import parse, tokenize
from unittest.case import TestCase
from funcparserlib.lexer import Token
from message import Message

def p(s):
    return parse(tokenize(s))

class ParserTest(TestCase):
    def test_eof_not_found(self):
        self.assertEqual(tokenize('2 print'),
                         [Token('number', '2'), Token('name', 'print')])
        self.assertEqual(p('2 print'),
                         [Message(2), Message('print')])

    def test_ignored_token_left(self):
        self.assertEqual(p('2 print;'),
                         [Message(2), Message('print')])
