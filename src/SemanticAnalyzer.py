from src.NodeVisitor import NodeVisitor
from src.Scope import Scope, ExecutionScope
from src.SemanticError import SemanticError
from src.Token import TokenType, Characters
from src.ast.expression import Expression
from src.ast.func import Func
from src.ast.ifStatement import IfStatement
from src.ast.returnStatement import ReturnStatement
from src.ast.variable import Variable
from src.ast.whileStatement import WhileStatement


class SemanticAnalyzer(NodeVisitor):
    def __init__(self, tree):
        self.executionScope = ExecutionScope(Scope([], []), Scope([], []))
        self.tree = tree

    def error(self, error_code, token):
        raise SemanticError(
            error_code=error_code,
            token=token,
            message=f'{error_code.value} -> {token}',
        )

    def analyze(self):
        for node in self.tree:
            self.visit(node)
        # (self.executionScope.currentScope)

    # sprawdzanie czy zmienna nie wystapila wczesniej w current scopie oraz typ wyrazenie przypisywanego
    def visitVariable(self, node):
        if self.executionScope.lookupVariable(node, True) is False:
            if node.value is not None:
                valueType = self.visit(node.value)  # sprawdzanie typu wyrazenie przypisywanego
                if valueType == node.getType():
                    self.executionScope.pushVariable(node)
                else:
                    raise SemanticError(
                        "przypisanie zlego typu"
                    )
            else:
                self.executionScope.pushVariable(node)
        else:
            raise SemanticError(
                "Zmienna ponownie zadeklarowana"
            )

    def visitExpression(self, node):
        type1 = self.visit(node.leftOperand)
        # print(f"[visitExpression: {type1}]")

        type2 = self.visit(node.rightOperand) if node.rightOperand else None

        # print(f"[visitExpression: {type2 }]")
        if type2 is None or type1 == type2:  # sprawdzanie zgodnosci typow, jesli drugi typ to None zwracany jest pierwszy
            return type1
        else:
            raise SemanticError(
                "rozne typy w wyrazeniu"
            )

    def visitValue(self, node):
        return TokenType.VAR_KW  # TODO: zmienna liczbowa ma typ VAR

    def checkArgumentsName(self, argumentList):
        argsNames = []
        isCorrect = True
        for arg in argumentList:
            if arg.varId not in argsNames:
                argsNames.append(arg.varId)
            else:
                isCorrect = False
        return isCorrect

    # sprawdza czy jest zadeklarowana
    def visitName(self, node):
        variable = self.executionScope.lookupVariableAndReturnVar(node, False)
        if variable is not None:
            # print(f"[visitName: {variable.getType()}, {variable.varType}]")
            return variable.getType()
        else:
            raise SemanticError(
                "zmienna nie jest zadeklarowana"
            )

    def visitCurrency(self, node):

        if self.executionScope.lookupVariable(node, True) is False:

            if node.value is not None:
                valueType = self.visit(node.value)  # sprawdzanie typu wyrazenie przypisywanego
                # print(list(Characters.currencies.values()))
                if valueType == TokenType.VAR_KW or valueType in Characters.currencies.values():
                    self.executionScope.pushVariable(node)
                else:
                    raise SemanticError(
                        "przypisanie zlego typu"
                    )

            else:
                self.executionScope.pushVariable(node)

        else:
            raise SemanticError(
                "Zmienna ponownie zadeklarowana"
            )

    def visitBool(self, node):
        if self.executionScope.lookupVariable(node, True) is False:
            if node.value is not None:
                valueType = self.visit(node.value)  # sprawdzanie typu wyrazenie przypisywanego
                # print(Characters.currencies.values())
                if valueType == TokenType.BOOL_KW:
                    self.executionScope.pushVariable(node)
                else:
                    raise SemanticError(
                        "przypisanie zlego typu"
                    )
            else:
                self.executionScope.pushVariable(node)
        else:
            raise SemanticError(
                "Zmienna ponownie zadeklarowana"
            )

    def visitAssignement(self, node):
        type1 = self.visit(node.name)
        type2 = self.visit(node.expression)

        if type1 == type2:  # sprawdzanie zgodnosci typow
            return type1
        else:
            raise SemanticError(
                "rozne typy w wyrazeniu"
            )

    # sprawdzamy czy funkcja istnieje, czy argumenty sa zadeklarowane
    def visitFuncCall(self, node):
        arguments = []
        for arg in node.args:
            argType = self.visit(arg)
            arguments.append(Variable(argType, ""))
        # jesli przypisujemy to co zwraca funkcja to zwracamy typ return statementu
        # print(arguments)
        # print(node.args)
        searchedDesiredFunction = Func(None, node.functionId, arguments)
        func = self.executionScope.lookupAndReturnFunction(searchedDesiredFunction)
        # print(func)
        if func is not None:
            # print(func.body.listOfStatements)
            if func.body:
                print(func)
                returnStatement = self.getReturnStatement(func)

                # print(returnStatement)
                # print("weszlo", self.visit(func.body.returnStatement))
                # print(returnStatement)
                return self.visit(
                    Expression(returnStatement.leftOperand, returnStatement.operation, returnStatement.rightOperand))
            else:
                return None

        else:

            raise SemanticError(
                "Funkcja nie jest zadeklarowana - bledne wywolanie"
            )

    def getReturnStatement(self, func):
        for statement in func.body.listOfStatements:

            if isinstance(statement, ReturnStatement):
                return statement
        return None

    def visitFunc(self, node):
        if self.checkArgumentsName(node.arguments) is True:
            if self.executionScope.lookupFunction(node, True) is False:
                self.executionScope.pushFunction(node)

                # zmiana scope przy zagnieżdzeniu
                parentScope = self.executionScope.getParentScope()
                currentScope = self.executionScope.getCurrentScope()

                self.executionScope = ExecutionScope(parentScope + currentScope, Scope([], []))
                # dodawanie argumentow do scope dla zagniezdzenia
                self.executionScope.pushVariables(node.arguments)

                returnType = self.visit(node.body)
                if returnType != node.funcType:
                    raise SemanticError(
                        "returnType nie jest zgodny z typem funkcji"
                    )

                self.executionScope = ExecutionScope(parentScope, currentScope)

            else:
                raise SemanticError(
                    "funkcja ponownie zadeklarowana"
                )
        else:
            raise SemanticError(
                "lista argumentow zawiera argumenty o tej samej nazwie"
            )

        # odwiedzanie kolejnych statementow w bloku i sprawdzenie typu return w ciałach while, if i funkcji

    def visitBlock(self, nodes):
        returnStatementTypes = []
        for node in nodes.listOfStatements:
            if isinstance(node, WhileStatement) or isinstance(node, IfStatement) or isinstance(node, ReturnStatement):
                print("byle co")
                returnStatementTypes.append(self.visit(node))

            else:
                self.visit(node)

        print("typy", returnStatementTypes)

        if len(set(returnStatementTypes)) > 1:
            raise SemanticError(
                "rozne zwracane typy w blokach "
            )
        elif len(set(returnStatementTypes)) == 1:
            return returnStatementTypes[0]

        else:
            return None

    def visitReturnStatement(self, node):
        return self.visitExpression(node)

    def visitWhileStatement(self, node):
        returnType = None
        self.visit(node.condition)
        parentScope = self.executionScope.getParentScope()
        currentScope = self.executionScope.getCurrentScope()

        self.executionScope = ExecutionScope(parentScope + currentScope, Scope([], []))

        returnType = self.visit(node.content)
        # print(self.executionScope.currentScope)
        self.executionScope = ExecutionScope(parentScope, currentScope)
        return returnType

    def visitBooleanExpr(self, node):
        self.visit(Expression(node.lValue, node.operator, node.rValue))

    def visitIfStatement(self, node):
        returnTypeIf = None
        returnTypeElse = None
        returnType = []
        self.visit(node.condition)
        parentScope = self.executionScope.getParentScope()
        currentScope = self.executionScope.getCurrentScope()

        self.executionScope = ExecutionScope(parentScope + currentScope, Scope([], []))

        returnType.append(self.visit(node.content))

        if node.elseBlock:
            returnType.append(self.visit(node.elseBlock))
            # print(self.executionScope.currentScope)
        self.executionScope = ExecutionScope(parentScope, currentScope)
        if len(returnType) == 2 and returnType[0] == returnType[1]:
            return returnType[0]
        elif len(returnType) == 2 and returnType[0] != returnType[1]:
            raise SemanticError(
                "rozne zwracane typy w blokach if i else"
            )
        elif len(returnType) == 1:
            return returnType[0]
        else:
            return None

    def visitPrintFunc(self, node):
        self.visit(node.identifier)