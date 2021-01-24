from src.NodeVisitor import NodeVisitor
from src.Scope import ExecutionScope, Scope
from src.SemanticError import SemanticError
from src.Token import TokenType
from src.ast.func import Func
from src.ast.ifStatement import IfStatement
from src.ast.name import Name
from src.ast.returnStatement import ReturnStatement
from src.ast.value import Value
from src.ast.variable import Variable
from src.ast.whileStatement import WhileStatement


class Interpreter(NodeVisitor):

    def __init__(self, tree, semanticAnalyzer):
        self.tree = tree
        self.executionScope = ExecutionScope(Scope([], []), Scope([], []))
        self.semanticAnalyzer = semanticAnalyzer

    def interpret(self):
        if self.tree is not None:
            for node in self.tree:
                self.visit(node)
        return ''

    def visitCurrency(self, node):
        pass

    def visitFunc(self, node):
        self.executionScope.pushFunction(node)


    def visitFuncCall(self, node):
        arguments = []
        self.semanticAnalyzer.executionScope = self.executionScope #aktualizacja scope dla semantic analyzera w celu ujednolicenia go ze scopem interpetera
        for arg in node.args:
            argType = self.semanticAnalyzer.visit(arg)
            arguments.append(Variable(argType, ""))
        func = self.executionScope.lookupAndReturnFunction(Func(None, node.functionId, arguments))

        return self.executeFunction(func, node.args)

    def executeFunction(self, func, args):

        parentScope = self.executionScope.getParentScope()
        currentScope = self.executionScope.getCurrentScope()

        parsedArguments = self.parseArgumentsToVariables(args, func.arguments ) # sparsowane argumenty wywołania do przekazania do funkcji

        self.executionScope = ExecutionScope(parentScope + currentScope, Scope(parsedArguments, []))
        #print("newparent", self.executionScope.parentScope)

        #print("newcurrent", self.executionScope.currentScope)
        returnValue = self.visit(func.body)
        self.executionScope = ExecutionScope(parentScope, currentScope)
        return returnValue


    def parseArgumentsToVariables(self,arguments, declarationArguments):
        copyOfArguments = declarationArguments.copy()
        for index in range(len(arguments)):
            copyOfArguments[index].value = Value(self.visit(arguments[index]))
        return copyOfArguments

    def visitBlock(self, node):
        for statement in node.listOfStatements:
            if isinstance(statement , ReturnStatement):
                return self.visit(statement)
            elif isinstance(statement, WhileStatement) or isinstance(statement, IfStatement):
                returned = self.visit(statement)
                if returned is not None:
                    return returned
            self.visit(statement)

    def visitReturnStatement(self, node):
        return self.visitExpression(node)


    def visitVariable(self, node):
        node.value = Value(self.visit(node.value))
        self.executionScope.pushVariable(node)

    def visitCurrency(self, node):

        node.value = Value(self.visit(node.value))
        self.executionScope.pushVariable(node)


    def visitValue(self, node):
        return float(node.value)

    def visitAssignement(self, node):
        expressionValue = self.visit(node.expression)
        self.executionScope.searchAndReplaceValue(node.name, Value(expressionValue))

    def visitPrintFunc(self, node):

        print(self.visit(node.identifier))


    def visitName(self, node):

        variable = self.executionScope.lookupVariableAndReturnVar(node, False)
        return self.visit(variable.value)





    def visitWhileStatement(self, node): #petla while sprawdzam warunek i dopoki nie natrafimy na return a warunek spelniony to wykonujemy


        condition = self.visit(node.condition)
        if condition == True:
            returned = self.visit(node.content)
            if returned is not None:
                return returned
            self.visit(node)


    def visitIfStatement(self, node):
        #print(node.condition)
        condition = self.visit(node.condition)
        #print("condition", condition)
        if condition == True:
            return self.visit(node.content)
        elif node.elseBlock is not None and condition == False :
            return self.visit(node.elseBlock)





    def visitBooleanExpr(self, node):
        #print(node.lValue)
        leftValue = self.visit(node.lValue)
        #print("left", leftValue)
        rightValue = self.visit(node.rValue) if node.rValue else None
        #print("right", rightValue)
#        print("tu", node.operator.getType())

        if rightValue == None:
            return leftValue

        elif node.operator.getType() == TokenType.GREATER:

            return  leftValue > rightValue

        elif node.operator.getType() == TokenType.LESS:

            return  leftValue < rightValue

        elif node.operator.getType() == TokenType.NOTEQUAL:

            return leftValue != rightValue

        elif node.operator.getType() == TokenType.EQUALS:

            return leftValue == rightValue


        elif node.operator.getType() == TokenType.GREATEROREQUAL:

            return leftValue >= rightValue

        elif node.operator.getType() == TokenType.LESSOREQUAL:
            return  leftValue <= rightValue

        elif node.operator.getType() == TokenType.OR:
            return leftValue or rightValue

        elif node.operator.getType() == TokenType.AND:
            return leftValue and rightValue

    def visitExpression(self, node):
        # print(f"[visitExpression: {type1}]")
        value1 = self.visit(node.leftOperand)
        #print(value1)
        value2 = self.visit(node.rightOperand) if node.rightOperand else None
       # print(value2)
        # print(f"[visitExpression: {type2 }]")
          # sprawdzanie zgodnosci typow, jesli drugi typ to None zwracany jest pierwszy

        if value2 == None:
            return value1
        elif node.operation == TokenType.PLUS:
            return value1+value2
        elif node.operation == TokenType.MINUS:
            return value1-value2
        elif node.operation == TokenType.MULTIPLY:
            return value1*value2
        elif node.operation == TokenType.DIVIDE:
            if value2 == 0:
                raise SemanticError(
                    "dzielenie przez 0"
                )
            else:
                return value1/value2


