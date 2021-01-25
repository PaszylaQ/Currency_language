import copy

from src.CurrencyReader import CurrencyReader
from src.NodeVisitor import NodeVisitor
from src.Scope import ExecutionScope, Scope
from src.SemanticError import SemanticError
from src.Token import TokenType, Characters
from src.ast.currency import Currency
from src.ast.func import Func
from src.ast.funcCall import FuncCall
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
                if isinstance(node, ReturnStatement):
                    return self.visit(node)
                else:
                    self.visit(node)
        return None


    def visitFunc(self, node, exchangeRate = None):
        self.executionScope.pushFunction(node)

    def visitFuncCall(self, node, exchangeRate = None):

        func = self.getFuncBodyByCall(node)

        executed = self.executeFunction(func, node.args)

        return executed
    def getFuncBodyByCall(self, node):
        arguments = []
        self.semanticAnalyzer.executionScope = copy.deepcopy(self.executionScope)  # aktualizacja scope dla semantic analyzera w celu ujednolicenia go ze scopem interpetera
        for arg in node.args:
            argType = self.semanticAnalyzer.visit(arg)
            arguments.append(Variable(argType, ""))
        return  self.executionScope.lookupAndReturnFunction(Func(None, node.functionId, arguments))

    def executeFunction(self, func, args):

        parentScope = self.executionScope.getParentScope()
        currentScope = self.executionScope.getCurrentScope()

        parsedArguments = self.parseArgumentsToVariables(args,
                                                         func.arguments)  # sparsowane argumenty wywołania do przekazania do funkcji

        self.executionScope = ExecutionScope(parentScope + currentScope, Scope(parsedArguments, []))

        returnValue = self.visit(copy.deepcopy(func.body))

        self.executionScope = ExecutionScope(parentScope, currentScope)
        return returnValue

    def parseArgumentsToVariables(self, arguments, declarationArguments):
        copyOfArguments = copy.deepcopy(declarationArguments)
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
        if len(self.executionScope.parentScope.variables) == 0 and len(self.executionScope.parentScope.functions) == 0:
            self.semanticAnalyzer.executionScope = copy.deepcopy(self.executionScope)
            variableType = self.semanticAnalyzer.visit(node)
            if variableType in currencies:
                currencyName = TokenType(variableType).name[0:-3]
                exchangeRate = self.currencies["exchange"][currencyName]
                variableValue = self.visitExpression(node) * exchangeRate
                variable = "{:.2f} {}".format(variableValue, currencyName)
                return variable


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
        return float(node.value)

    def visitAssignement(self, node, exchangeRate = None):
        expressionValue = self.visit(node.expression)
        self.executionScope.searchAndReplaceValue(node.name, Value(expressionValue))

    def visitPrintFunc(self, node, exchangeRate = None):
        temp = None
        if isinstance(node.identifier, FuncCall):
            func = self.getFuncBodyByCall(node.identifier)
            temp = Currency(func.funcType, ' ', Value(self.executeFunction(func, node.identifier.args)))
        else:
            temp = self.executionScope.lookupVariableAndReturnVar(node.identifier, False)

        if isinstance(temp, Currency):
            currencyName = TokenType(temp.varType).name[0:-3]
            exchangeRate = self.currencies["exchange"][currencyName]
            variableValue = self.visit(temp.value) * exchangeRate
            variable = "{:.2f} {}".format(variableValue, currencyName)
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
        parentScope = self.executionScope.getParentScope()
        currentScope = self.executionScope.getCurrentScope()
        condition = self.visit(node.condition)
        if condition == True:
            self.executionScope = ExecutionScope(parentScope + currentScope, Scope([], []))
            returned = self.visit(node.content)
            if returned is not None:
                return returned
            self.executionScope = ExecutionScope(parentScope, currentScope)
            self.visit(node) #wywolanie while statement ponownie dopoki condition true

    def visitIfStatement(self, node, exchangeRate = None):
        # print(node.condition)

        parentScope = self.executionScope.getParentScope()
        currentScope = self.executionScope.getCurrentScope()

        condition = self.visit(node.condition)
        # print("condition", condition)
        self.executionScope = ExecutionScope(parentScope + currentScope, Scope([], []))
        if condition == True:

            returned =  self.visit(node.content)

        elif node.elseBlock is not None and condition == False:

            returned = self.visit(node.elseBlock)

        self.executionScope = ExecutionScope(parentScope, currentScope)
        return returned

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

    def visitExpression(self, node, exchangeRate = None): #dodana funkcjonalnosc mnozenia var i currency przy inicjalizacji zmiennej walutowej
        # print(f"[visitExpression: {type1}]")

        # print(value1)
        # skorzystanie z analizatora wiąże się z zamianą scope w celu utrzymania zmiennnych wraz z zagłębieniem

        self.semanticAnalyzer.executionScope = copy.deepcopy(self.executionScope)
        type1 = self.semanticAnalyzer.visit(node.leftOperand)
        type2 = self.semanticAnalyzer.visit(node.rightOperand) if node.rightOperand else None


        value1 = None
        value2 = None
        if type1 == TokenType.VAR_KW and type2 in currencies:


            value1 = self.visit(node.leftOperand, exchangeRate) / exchangeRate
            value2 = self.visit(node.rightOperand, exchangeRate)
        elif type2 == TokenType.VAR_KW and type1 in currencies:
            value1 = self.visit(node.leftOperand, exchangeRate)
            value2 = self.visit(node.rightOperand, exchangeRate) / exchangeRate
        elif type1 == TokenType.VAR_KW and type2 == None and exchangeRate is not None:
            value1 = self.visit(node.leftOperand, None) / exchangeRate
        else:

            value1 = self.visit(node.leftOperand, exchangeRate)
            value2 = self.visit(node.rightOperand, exchangeRate) if node.rightOperand else None

        #print("Value1:", value1)
        #print("Value2:", value2)
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
                raise RuntimeError(
                    "dzielenie przez 0"
                )
            else:
                return value1 / value2
