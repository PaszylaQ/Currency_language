import io
import sys
from unittest import TestCase

from src.Lexer import Lexer
from src.Parser import Parser
from src.Source import Source
from src.Token import Token
from src.Token import TokenType
from src.ast.block import Block
from src.ast.booleanExpr import BooleanExpr
from src.ast.expression import Expression
from src.ast.func import Func
from src.ast.name import Name
from src.ast.returnStatement import ReturnStatement
from src.ast.value import Value
from src.ast.variable import Variable
from src.ast.whileStatement import WhileStatement


class ParserTests(TestCase):

    def testParseVariableBool(self):
        sys.stdin = io.StringIO("bool var1;"
                                )

        source = Source()
        lexer = Lexer(source)
        parser = Parser(source, lexer)

        var1 = Variable(TokenType.BOOL_KW, Name("var1"), None)
        var_1 = parser.parseVariableDeclaration()
        self.assertEqual(var_1, var1)

    def testParseVariableVar(self):
        sys.stdin = io.StringIO("var var1;"
                                )

        source = Source()
        lexer = Lexer(source)
        parser = Parser(source, lexer)

        var1 = Variable(TokenType.VAR_KW, Name("var1"), None)
        var_1 = parser.parseVariableDeclaration()
        self.assertEqual(var_1, var1)

    def testParseExampleVariableCurr(self):
        sys.stdin = io.StringIO("PLN var1;")

        source = Source()
        lexer = Lexer(source)
        parser = Parser(source, lexer)

        var1 = Variable(TokenType.PLN_KW, Name("var1"), None)
        var_1 = parser.parseVariableDeclaration()
        self.assertEqual(var_1, var1)

    def testParseFuncDeclarationWithArgs(self):
        sys.stdin = io.StringIO("def savingsInPolishCurrency(bool currency1){"
                                "var extra;"
                                "return extra;"
                                "}")

        source = Source()
        lexer = Lexer(source)
        parser = Parser(source, lexer)
        fu_nc = (parser.parseFunc())
        func = Func(Name("savingsInPolishCurrency"),
                    [Variable(TokenType.BOOL_KW, Name("currency1"), None)],
                    Block([Variable(TokenType.VAR_KW, Name("extra"), None),
                           ReturnStatement(Expression(Expression("extra")))]))

        self.assertEqual(func, fu_nc)

    def testParseAssignement(self):
        sys.stdin = io.StringIO(" var x = 2+2*2;")
        source = Source()
        lexer = Lexer(source)
        parser = Parser(source, lexer)
        declaration = (parser.parseVariableDeclaration())
        declaration_ = Variable(TokenType.VAR_KW, Name("x"),
                                Expression(Expression(Value("2"), None, None), TokenType.PLUS,
                                           Expression(Value("2"), TokenType.MULTIPLY, Value("2"))))

        self.assertEqual(declaration_, declaration)

    def testParseWhile(self):
        statement_ = WhileStatement(BooleanExpr(BooleanExpr(
            BooleanExpr(Expression(Expression("i"), None, None), Token(TokenType.GREATEROREQUAL, ">="),
                        Expression(Expression(Value("5"), None, None), None, None)), None, None), None, None), Block(
            [Variable(TokenType.PLN_KW, Name("pln"), Expression(Expression(Value("5"), None, None), None, None)),
             ReturnStatement(Expression(Expression("variable", None, None), None, None), None, None)]), None)

        sys.stdin = io.StringIO("while(i>=5){ "
                                "PLN pln = 5;"
                                "return variable;"
                                "}")
        source = Source()
        lexer = Lexer(source)
        parser = Parser(source, lexer)
        statement = parser.parseWhileStatement()
        print(statement)

        self.assertEqual(statement_, statement)
