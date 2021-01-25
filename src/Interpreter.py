from src.CurrencyReader import CurrencyReader
from src.NodeVisitor import NodeVisitor
from src.Scope import ExecutionScope, Scope
from src.SemanticError import SemanticError
from src.Token import TokenType, Characters
from src.ast.currency import Currency
from src.ast.func import Func
from src.ast.ifStatement import IfStatement
from src.ast.returnStatement import ReturnStatement
from src.ast.value import Value
from src.ast.variable import Variable
from src.ast.whileStatement import WhileStatement
from src.utils.getCurrenciesPath import getCurrenciesPath

characters = Characters()
currencies = characters.currencyTypesToList()
currenciesDict = characters.currencies


class Interpreter(NodeVisitor):

    def __init__(self, tree, semanticAnalyzer):
        self.tree = tree
        self.executionScope = ExecutionScope(Scope([], []), Scope([], []))
        self.semanticAnalyzer = semanticAnalyzer
        self.currencies = CurrencyReader(getCurrenciesPath()).getCurrencies()

    def interpret(self):
        if self.tree is not None:
            for node in self.tree:
                self.visit(node)
        return ''


    def visitFunc(self, node, exchangeRate = None):
        self.executionScope.pushFunction(node)

    def visitFuncCall(self, node, exchangeRate = None):
        arguments = []
        self.semanticAnalyzer.executionScope = self.executionScope  # aktualizacja scope dla semantic analyzera w celu ujednolicenia go ze scopem interpetera
        for arg in node.args:
            argType = self.semanticAnalyzer.visit(arg)
            arguments.append(Variable(argType, ""))
        func = self.executionScope.lookupAndReturnFunction(Func(None, node.functionId, arguments))

        return self.executeFunction(func, node.args)

    def executeFunction(self, func, args):

        parentScope = self.executionScope.getParentScope()
        currentScope = self.executionScope.getCurrentScope()

        parsedArguments = self.parseArgumentsToVariables(args,
                                                         func.arguments)  # sparsowane argumenty wywołania do przekazania do funkcji

        self.executionScope = ExecutionScope(parentScope + currentScope, Scope(parsedArguments, []))
        # print("newparent", self.executionScope.parentScope)

        # print("newcurrent", self.executionScope.currentScope)
        returnValue = self.visit(func.body)
        self.executionScope = ExecutionScope(parentScope, currentScope)
        return returnValue

    def parseArgumentsToVariables(self, arguments, declarationArguments):
        copyOfArguments = declarationArguments.copy()
        for index in range(len(arguments)):
            copyOfArguments[index].value = Value(self.visit(arguments[index]))
        return copyOfArguments

    def visitBlock(self, node, exchangeRate = None):
        for statement in node.listOfStatements:
            if isinstance(statement, ReturnStatement):
                return self.visit(statement)
            elif isinstance(statement, WhileStatement) or isinstance(statement, IfStatement):
                returned = self.visit(statement)
                if returned is not None:
                    return returned
            self.visit(statement)

    def visitReturnStatement(self, node, exchangeRate = None):
        return self.visitExpression(node)

    def visitVariable(self, node, exchangeRate = None):
        node.value = Value(self.visit(node.value))
        self.executionScope.pushVariable(node)

    def visitCurrency(self, node, exchangeRate = None):

        if node.value is None:
            self.executionScope.pushVariable(node)

        elif node.varType in currencies:
            currencyName = TokenType(node.varType).name[0:-3]
            exchangeRate = self.currencies["exchange"][currencyName]
            node.value = Value(self.visit(node.value,exchangeRate))
            self.executionScope.pushVariable(node)

        else:
            node.value = Value(self.visit(node.value))
            self.executionScope.pushVariable(node)

    def visitValue(self, node, exchangeRate = None):
        return float(node.value)/exchangeRate if exchangeRate is not None else float(node.value)

    def visitAssignement(self, node, exchangeRate = None):
        expressionValue = self.visit(node.expression)
        self.executionScope.searchAndReplaceValue(node.name, Value(expressionValue))

    def visitPrintFunc(self, node, exchangeRate = None):
        temp = self.executionScope.lookupVariableAndReturnVar(node.identifier, False)

        if isinstance(temp, Currency):
            currencyName = TokenType(temp.varType).name[0:-3]
            exchangeRate = self.currencies["exchange"][currencyName]
            variable = self.visit(temp.value) * exchangeRate
            variable = f"{variable} {currencyName}"
            print(variable)

        elif isinstance(temp, Variable):
            print(self.visit(temp.varId))

        else:
            print(self.visit(node))

    def visitNoneType(self, exchangeRate = None):
        raise RuntimeError(
            "proba dostania się do wartosci None"
        )


    def visitName(self, node, exchangeRate = None):

        variable = self.executionScope.lookupVariableAndReturnVar(node, False)
        #print(variable)
        return self.visit(variable.value)

    def visitWhileStatement(self,
                            node, exchangeRate = None):  # petla while sprawdzam warunek i dopoki nie natrafimy na return a warunek spelniony to wykonujemy

        condition = self.visit(node.condition)
        if condition == True:
            returned = self.visit(node.content)
            if returned is not None:
                return returned
            self.visit(node)

    def visitIfStatement(self, node, exchangeRate = None):
        # print(node.condition)
        condition = self.visit(node.condition)
        # print("condition", condition)
        if condition == True:
            return self.visit(node.content)
        elif node.elseBlock is not None and condition == False:
            return self.visit(node.elseBlock)

    def visitBooleanExpr(self, node, exchangeRate = None):
        # print(node.lValue)
        leftValue = self.visit(node.lValue)
        # print("left", leftValue)
        rightValue = self.visit(node.rValue) if node.rValue else None
        # print("right", rightValue)
        #        print("tu", node.operator.getType())

        if rightValue == None:
            return leftValue

        elif node.operator.getType() == TokenType.GREATER:

            return leftValue > rightValue

        elif node.operator.getType() == TokenType.LESS:

            return leftValue < rightValue

        elif node.operator.getType() == TokenType.NOTEQUAL:

            return leftValue != rightValue

        elif node.operator.getType() == TokenType.EQUALS:

            return leftValue == rightValue


        elif node.operator.getType() == TokenType.GREATEROREQUAL:

            return leftValue >= rightValue

        elif node.operator.getType() == TokenType.LESSOREQUAL:
            return leftValue <= rightValue

        elif node.operator.getType() == TokenType.OR:
            return leftValue or rightValue

        elif node.operator.getType() == TokenType.AND:
            return leftValue and rightValue

    def visitExpression(self, node, exchangeRate = None):
        # print(f"[visitExpression: {type1}]")
        value1 = self.visit(node.leftOperand, exchangeRate)
        # print(value1)
        value2 = self.visit(node.rightOperand, exchangeRate) if node.rightOperand else None

        if value2 == None:
            return value1
        elif node.operation == TokenType.PLUS:
            return value1 + value2
        elif node.operation == TokenType.MINUS:
            return value1 - value2
        elif node.operation == TokenType.MULTIPLY:
            return value1 * value2
        elif node.operation == TokenType.DIVIDE:
            if value2 == 0:
                raise SemanticError(
                    "dzielenie przez 0"
                )
            else:
                print(value1, value2)
                return value1 / value2
