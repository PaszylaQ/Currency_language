import unittest
from src.Lexer import Lexer

from src.Token import TokenType


class MyTestCase(unittest.TestCase):

    def testNames(self):

        lexer = Lexer("testObjectId.txt")
        names = ['Maciej', 'currency', 'currency2', 'While2', 'if123']

        for i in range(len(names)-1):
            lexer.tokenize()
            self.assertEqual(lexer.getToken().tokenType, TokenType.NAME)
            self.assertEqual(lexer.getToken().value, names[i])


    def testKeywords(self):
        lexer = Lexer("testKeywords.txt")
        keywords = {

        'def': TokenType.DEF_KW,
        'print': TokenType.PRINT_KW,
        'var': TokenType.VAR_KW,
        'while': TokenType.WHILE_KW,
        'if': TokenType.IF_KW,
        'else': TokenType.ELSE_KW,
        'return': TokenType.RETURN_KW,
        'string': TokenType.STRING,

        }
        for i in range(len(keywords)-1):

            lexer.tokenize()
            self.assertEqual(lexer.getToken().tokenType, list(keywords.values())[i])
            self.assertEqual(lexer.getToken().value, list(keywords.keys())[i])


    def testNumbers(self):
        lexer = Lexer("testNumbers.txt")
        numbers = ['12.0', '3', '13.7', '15.8']
        for i in range(len(numbers)-1):

            lexer.tokenize()
            self.assertEqual(lexer.getToken().tokenType, TokenType.NUMBER)
            self.assertEqual(lexer.getToken().value, numbers[i])


    def testText(self):
        lexer = Lexer("testText.txt")
        text = "Przykładowy tekst dla lexera"

        lexer.tokenize()
        self.assertEqual(lexer.getToken().tokenType, TokenType.TEXT)
        self.assertEqual(lexer.getToken().value, text)


    def testCharacters(self):
        lexer = Lexer("testCharacters.txt")
        characters = {
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.MULTIPLY,
            '/': TokenType.DIVIDE,
            '!': TokenType.NOT,
            '>': TokenType.GREATER,
            '<': TokenType.LESS,
            '&': TokenType.AND,
            '|': TokenType.OR,
            '[': TokenType.LEFTBRACKET,
            ']': TokenType.RIGHTBRACKET,
            '(': TokenType.LEFTPARENTHESIS,
            ')': TokenType.RIGHTPRAENTHESIS,
            '{': TokenType.LEFTCURLY,
            '}': TokenType.RIGHTCURLY,
            ',': TokenType.COMMA,
            '=': TokenType.ASSIGN,
            ';': TokenType.SEMICOLON,
            ':': TokenType.COLON,
            '.': TokenType.DOT

        }
        for i in range(len(characters)-1):

            lexer.tokenize()
            self.assertEqual(lexer.getToken().tokenType, list(characters.values())[i])
            self.assertEqual(lexer.getToken().value, list(characters.keys())[i])

    def testDoubleOperators(self):
        lexer = Lexer("testDoubleOperators.txt")
        doubleOperators = {
            '==': TokenType.EQUALS,
            '!=': TokenType.NOTEQUAL,
            '>=': TokenType.GREATEROREQUAL,
            '<=': TokenType.LESSOREQUAL
        }
        for i in range(len(doubleOperators)-1):

            lexer.tokenize()
            self.assertEqual(lexer.getToken().tokenType, list(doubleOperators.values())[i])
            self.assertEqual(lexer.getToken().value, list(doubleOperators.keys())[i])

    def testUnknownInput(self):
        unknownInput = ['$' ,'%','^']
        lexer = Lexer("testUnknownInput.txt")
        for i in range(len(unknownInput)-1):
            lexer.tokenize()
            self.assertEqual(lexer.getToken().tokenType, TokenType.UNKNOWN)
            self.assertEqual(lexer.getToken().value, unknownInput[i])

