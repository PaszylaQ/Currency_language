import unittest
from Lexer import  Lexer


class LexerTest(unittest.TestCase):

    m = Lexer()
    m.build()

    def test_keyword_type_and_value_after_tokenizing(self):
        keywords = {

            'def': 'DEF',
            'print': 'PRINT',
            'var': 'VAR',
            'while': "WHILE",
            'if': "IF",
            'else': 'ELSE'
        }
        for key in keywords.keys():
            self.assertEqual(self.m.tokenize(key).value , key )
            self.assertEqual(self.m.tokenize(key).type, keywords[key])

    def test_name_tokenizing(self):
        names = ["Maciej", "USD", "zlote", "dolary", "k"]
        for name in names:
            self.assertEqual(self.m.tokenize(name).value, name)
            self.assertEqual(self.m.tokenize(name).type, 'NAME')

    def test_operators(self):
        operators = {
            '*' : 'MULTIPLY',
            '/' : 'DIVIDE',
            '+' : 'PLUS',
            '-' : 'MINUS',
            '=' : 'ASSIGN',
            '==': 'EQUALS',
            '!=': 'NOTEQUAL',
            '>=': 'GREATEROREQUAL',
            '<=': 'LESSOREQUAL',
            '>' : 'GREATER',
            '<' : 'LESS',
            '&' : 'AND',
            '|' : 'OR'
        }
        for operator in operators.keys():
            self.assertEqual(self.m.tokenize(operator).value , operator )
            self.assertEqual(self.m.tokenize(operator).type, operators[operator])

    def test_numbers(self):
        numbers= ['2.3' , '5.4', '12.0', '16.5']
        for number in numbers:
            self.assertEqual(self.m.tokenize(number).value, float(number))
            self.assertEqual(self.m.tokenize(number).type, 'NUMBER')

