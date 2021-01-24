from typing import List

from src.Lexer import Lexer
from src.Source import Source
from src.Token import TokenType
from src.ast.assignement import Assignement
from src.ast.block import Block
from src.ast.bool import Bool
from src.ast.booleanExpr import BooleanExpr
from src.ast.currency import Currency
from src.ast.expression import Expression
from src.ast.func import Func
from src.ast.funcCall import FuncCall
from src.ast.ifStatement import IfStatement
from src.ast.name import Name
from src.ast.printFunc import PrintFunc
from src.ast.returnStatement import ReturnStatement
from src.ast.value import Value
from src.ast.variable import Variable
from src.ast.whileStatement import WhileStatement
from src.exception import InvalidSyntax


class Parser():
    def __init__(self, source: Source, lexer: Lexer):
        self.source = source
        self.lexer = lexer
        self.lexer.tokenize()
        self.currentToken = self.lexer.getToken()

    def checkTokenType(self, tokenType):
        return self.currentToken.getType() == tokenType

    def consume(self):
        oldToken = self.currentToken
        self.lexer.tokenize()
        newToken = self.lexer.getToken()
        self.currentToken = newToken
        return oldToken

    def checkIfRequiredToken(self, tokenType: TokenType):
        if self.currentToken.getType() == tokenType:
            return self.currentToken
        else:
            raise InvalidSyntax(
                f"On position {self.source.getPositionInLine()} "
                f"expected '{tokenType}', "
                f"got {self.currentToken.getType()}: "
                f"{self.currentToken.getValue()}")

    def checkIfRequiredTokensInCertainTypes(self,
                                            listOfTypes: List[TokenType]):
        for tokenType in listOfTypes:
            if tokenType == self.currentToken.getType():
                token = self.currentToken

                return token
        raise InvalidSyntax(f"On position {self.source.getPositionInLine()} "
                            f"expected '{listOfTypes}', "
                            f"got {self.currentToken.getType()}: "
                            f"{self.currentToken.getValue()}")

    def checkIfRequiredAndConsume(self, tokenType: TokenType):
        self.checkIfRequiredToken(tokenType)
        return self.consume()

    def checkIfRequiredAndConsumeTokensInCertainTypes(
            self, listOfTypes: List[TokenType]):
        for tokenType in listOfTypes:
            if tokenType == self.currentToken.getType():
                token = self.currentToken
                self.consume()
                return token.getType()
        raise InvalidSyntax(f"On position {self.source.getPositionInLine()} "
                            f"expected '{listOfTypes}', "
                            f"got {self.currentToken.getType()}: "
                            f"{self.currentToken.getValue()}")

    def checkTokens(self, listOfTokens: List[TokenType]):
        if self.currentToken.getType() in listOfTokens:
            return True

    def parse(self):
        functions = []
        while self.currentToken.getType() != TokenType.EOF:
            function = self.parseProgramStatement()
            functions.append(function)
        return functions

    def parseProgramStatement(self):
        if self.currentToken.getType() == TokenType.DEF_KW:
            return self.parseFunc()
        else:
            return self.parseStatement()

    def parseStatement(self):
        currentTokenType = self.currentToken.getType()

        if currentTokenType == TokenType.IF_KW:
            return self.parseIfStatement()
        elif currentTokenType == TokenType.WHILE_KW:
            return self.parseWhileStatement()
        else:
            return self.parseSimpleStatement()

    def parseSimpleStatement(self):
        currentTokenType = self.currentToken.getType()
        variableTypes = [
            TokenType.VAR_KW, TokenType.BOOL_KW, TokenType.PLN_KW,
            TokenType.USD_KW
        ]
        if currentTokenType == TokenType.NAME:
            statement = self.parseAssignementOrFuncCall()
        elif currentTokenType == TokenType.PRINT_KW:
            statement = self.parsePrintStatement()
        elif currentTokenType in variableTypes:
            statement = self.parseVariableDeclaration()
        elif self.currentToken.getType() == TokenType.RETURN_KW:
            statement = self.parseReturnStatement()
        else:
            raise InvalidSyntax

        return self.parseSemicolon(statement)

    def parseSemicolon(self, statement):
        if self.currentToken.getType() == TokenType.SEMICOLON:
            self.consume()
            return statement
        else:
            raise InvalidSyntax

    def parsePrintStatement(self):
        text = None
        self.checkIfRequiredAndConsume(TokenType.PRINT_KW)
        self.checkIfRequiredAndConsume(TokenType.LEFTPARENTHESIS)
        if self.currentToken.getType() == TokenType.TEXT:
            text = self.consume()
        else:
            text = self.parseOppExpression()
        if text is None:
            raise InvalidSyntax
        else:
            self.checkIfRequiredAndConsume(TokenType.RIGHTPRAENTHESIS)
            return PrintFunc(text)

    def parseConditionalStatement(self):
        if self.currentToken.getType() == TokenType.IF_KW:
            return self.parseIfStatement()
        else:
            return self.parseWhileStatement()

    def parseIfStatement(self):
        self.checkIfRequiredAndConsume(TokenType.IF_KW)
        self.checkIfRequiredAndConsume(TokenType.LEFTPARENTHESIS)
        cond = self.parseOrExpression()
        self.checkIfRequiredAndConsume(TokenType.RIGHTPRAENTHESIS)
        elseBlock = None
        block = self.parseBlock()
        if self.currentToken.getType() == TokenType.ELSE_KW:
            self.consume()
            elseBlock = self.parseBlock()
        return IfStatement(cond, block, elseBlock)

    def parseOrExpression(self):
        expr1 = self.parseAndExpression()
        expr2 = None
        operator = None

        if self.currentToken.getType() == TokenType.OR:
            operator = self.consume()
            expr2 = self.parseAndExpression()

        return BooleanExpr(expr1, operator, expr2)

    def parseAndExpression(self):
        expr1 = self.parseCondition()
        expr2 = None
        operator = None

        if self.currentToken.getType() == TokenType.AND:
            operator = self.consume()
            expr2 = self.parseCondition()

        return BooleanExpr(expr1, operator, expr2)

    def parseCondition(self):
        expr1 = self.parseExpression()
        operator = None
        expr2 = None

        requiredTokens = [TokenType.GREATEROREQUAL, TokenType.LESSOREQUAL, TokenType.NOTEQUAL, TokenType.EQUALS,
                          TokenType.GREATER, TokenType.LESS]

        if self.currentToken.getType() in requiredTokens:
            operator = self.consume()
            expr2 = self.parseExpression()
        return BooleanExpr(expr1, operator, expr2)

    def parseBlock(self):
        self.checkIfRequiredAndConsume(TokenType.LEFTCURLY)
        listOfStatements = []
        returnStatement = None
        while self.currentToken.getType() not in [TokenType.RIGHTCURLY]:
            listOfStatements.append(self.parseStatement())
        if self.currentToken.getType() == TokenType.RETURN_KW:
            returnStatement = self.parseReturnStatement()  # parsowanie funkcji nie konczy sie na return tylko na left curly
        self.checkIfRequiredAndConsume(TokenType.RIGHTCURLY)
        return Block(listOfStatements, returnStatement)

    def parseReturnStatement(self):
        self.consume()
        expression = self.parseExpression()
        return ReturnStatement(expression)

    def parseWhileStatement(self):
        self.checkIfRequiredAndConsume(TokenType.WHILE_KW)
        self.checkIfRequiredAndConsume(TokenType.LEFTPARENTHESIS)
        cond = self.parseOrExpression()
        self.checkIfRequiredAndConsume(TokenType.RIGHTPRAENTHESIS)
        block = self.parseBlock()
        return WhileStatement(cond, block)

    def parseAssignementOrFuncCall(self):
        name = self.currentToken.getValue()
        self.consume()
        if self.currentToken.getType() == TokenType.ASSIGN:
            self.consume()
            expr = self.parseExpression()
            return Assignement(Name(name), expr)
        else:
            return self.parseFunCall(name)

    def parseVariableDeclaration(self):
        variableType = self.parseType()
        variableName = self.parseId()
        value = None
        if self.currentToken.getType() == TokenType.ASSIGN:
            self.checkIfRequiredAndConsume(TokenType.ASSIGN)
            value = self.parseExpression()
        if variableType == TokenType.VAR_KW:
            return Variable(variableType, variableName, value)
        elif variableType == TokenType.BOOL_KW:
            return Bool(value)
        else:
            return Currency(variableType, variableName, value)

    def parseType(self):
        variableTypes = [
            TokenType.VAR_KW, TokenType.BOOL_KW, TokenType.PLN_KW,
            TokenType.USD_KW
        ]
        type = self.checkIfRequiredAndConsumeTokensInCertainTypes(
            variableTypes)
        return type

    def parseId(self):
        token = self.checkIfRequiredAndConsume(TokenType.NAME)
        identifier = Name(token.getValue())
        return identifier

    def parseExpression(self):
        expr1 = self.parseMultiplicativeExpression()
        expr2 = None
        operation = None
        if self.currentToken.getType() == TokenType.PLUS or self.currentToken.getType() == TokenType.MINUS:
            operation = self.currentToken.getType()
            self.consume()
            expr2 = self.parseMultiplicativeExpression()
        return Expression(expr1, operation, expr2)

    def parseMultiplicativeExpression(self):
        expr1 = self.parseOppExpression()
        expr2 = None
        operation = None
        if self.currentToken.getType() == TokenType.MULTIPLY or self.currentToken.getType() == TokenType.DIVIDE:
            operation = self.currentToken.getType()
            self.consume()
            expr2 = self.parseOppExpression()
        return Expression(expr1, operation, expr2)

    def parseOppExpression(self):
        tokens = [TokenType.PLUS, TokenType.MULTIPLY, TokenType.MINUS, TokenType.DIVIDE]
        if self.currentToken.getType() == TokenType.NUMBER:
            tokenValue = self.currentToken.getValue()
            self.consume()
            return Value(tokenValue)
        elif self.currentToken.getType() == TokenType.NAME:
            return self.parseNameOrFunCall()
        elif self.currentToken.getType() == TokenType.LEFTPARENTHESIS:
            self.consume()
            expression = self.parseExpression()
            if self.currentToken.getType() != TokenType.RIGHTPRAENTHESIS:
                raise InvalidSyntax
            else:
                self.consume()
                return expression
        # elif self.currentToken.getType() in tokens:
        #     self.consume()

    def parseNameOrFunCall(self):
        name = self.currentToken.getValue()
        self.consume()
        if self.currentToken.getType() == TokenType.LEFTPARENTHESIS:
            return self.parseFunCall(name)

        return Name(name)

    def parseFunCall(self, name):
        self.checkIfRequiredAndConsume(TokenType.LEFTPARENTHESIS)
        arguments = []
        if self.currentToken.getType() == TokenType.RIGHTPRAENTHESIS:
            self.consume()
        else:
            arguments = self.parseFunCallArgs()

        return FuncCall(Name(name), arguments)

    def parseFunCallArgs(self):
        arguments = []
        arguments.append(self.parseExpression())
        if self.currentToken.getType() == TokenType.COMMA:
            while self.currentToken.getType() != TokenType.RIGHTPRAENTHESIS:
                self.checkIfRequiredAndConsume(TokenType.COMMA)
                arguments.append((self.parseExpression()))
        self.checkIfRequiredAndConsume(TokenType.RIGHTPRAENTHESIS)
        return arguments

    def parseArgument(self):  # TODO: dodac typy currencies

        self.checkIfRequiredAndConsume(TokenType.LEFTPARENTHESIS)
        variable_types = [
            TokenType.RIGHTPRAENTHESIS, TokenType.VAR_KW, TokenType.NUMBER,
            TokenType.BOOL_KW, TokenType.PLN_KW
        ]
        arguments = []
        self.checkIfRequiredTokensInCertainTypes(variable_types)
        if self.currentToken.getType() != TokenType.RIGHTPRAENTHESIS:
            variableType = self.currentToken.getType()
            self.consume()
            token = self.checkIfRequiredAndConsume(TokenType.NAME)
            variableName = Name(token.getValue())  # TODO: dodaj typ currency
            if variableType == TokenType.VAR_KW:
                arguments.append(Variable(variableType, variableName, None, None))
            else:
                arguments.append(Currency(variableType, variableName, None, None))

            while True:
                requiredTokens = [TokenType.COMMA, TokenType.RIGHTPRAENTHESIS]
                self.checkIfRequiredTokensInCertainTypes(requiredTokens)
                if self.currentToken.getType() == TokenType.RIGHTPRAENTHESIS:
                    break
                variable_types = [
                    TokenType.VAR_KW, TokenType.NUMBER, TokenType.BOOL_KW, TokenType.PLN_KW
                ]
                self.consume()
                self.checkIfRequiredTokensInCertainTypes(variable_types)
                nextvariableType = self.currentToken.getType()
                self.consume()
                token = self.checkIfRequiredAndConsume(TokenType.NAME)
                nextvariableName = Name(token.getValue())
                if nextvariableType == TokenType.VAR_KW:
                    arguments.append(Variable(nextvariableType, nextvariableName, None, None))
                else:
                    arguments.append(Currency(nextvariableType, nextvariableName, None, None))

        return arguments

    def parseFunc(self):
        requiredTokens = [TokenType.DEF_KW]

        self.checkIfRequiredAndConsumeTokensInCertainTypes(requiredTokens)

        funcType = self.parseType()
        identifier = self.parseId()
        arguments = self.parseArgument()
        self.checkIfRequiredAndConsume(TokenType.RIGHTPRAENTHESIS)
        body = self.parseBlock()
        return Func(funcType, identifier, arguments, body, None, None)
