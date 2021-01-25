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

characters = Characters()
currencies = characters.currencyTypesToList()
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
        multiplicativeOperators = [TokenType.MULTIPLY, TokenType.DIVIDE]
        additiveOperators = [TokenType.PLUS, TokenType.MINUS]
        # print(f"[visitExpression: {type2 }]")
        if type1 in currencies and type2 == TokenType.VAR_KW  and node.operation in multiplicativeOperators:
            return TokenType.EUR_KW
        elif   type2 in currencies and type2 == TokenType.VAR_KW and node.operation in multiplicativeOperators:
            return TokenType.EUR_KW
        elif type1 in currencies and type2 in currencies and node.operation in additiveOperators:
            return TokenType.EUR_KW
        elif type2 is None or type1 == type2 and type1 not in currencies:  # sprawdzanie zgodnosci typow, jesli drugi typ to None zwracany jest pierwszy
            return type1
        elif type2 is None or type1 == type2 and type1  in currencies:
            return TokenType.EUR_KW
        elif type1 in currencies and type2 in currencies and node.operation in multiplicativeOperators:
            raise SemanticError(
                "proba mnożenia lub dzielenia walut - niedozwolone"
            )
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
            # print(self.executionScope.parentScope)
            # print(self.executionScope.currentScope)
            raise SemanticError(
                "zmienna nie jest zadeklarowana"
            )

    def visitCurrency(self, node):

        if self.executionScope.lookupVariable(node, True) is False:

            if node.value is not None:
                valueType = self.visit(node.value)  # sprawdzanie typu wyrazenie przypisywanego
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

        if type1 == type2 or (type1 in currencies and type2 in currencies):   # sprawdzanie zgodnosci typow
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

        searchedDesiredFunction = Func(None, node.functionId, arguments)
        func = self.executionScope.lookupAndReturnFunction(searchedDesiredFunction)
        if func is not None:
            return func.funcType
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

                if returnType != node.funcType and not (returnType == TokenType.EUR_KW and node.funcType in currencies):
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
        blockReturnStatementTypes = []
        returnStatementTypes = []
        for node in nodes.listOfStatements:
            if isinstance(node, WhileStatement) or isinstance(node, IfStatement):
                blockReturnStatementTypes.append(self.visit(node))

            elif isinstance(node, ReturnStatement):
                returnStatementTypes.append(self.visit(node))

            else:
                self.visit(node)

        # sprawdzenie czy typ zwracany z blokow w funkcji w przypadku jego zwracanai pokrywa się z returnem w funkcji
        if len(set(returnStatementTypes)) == 1:
            returnStatementTypes.append(None)
            if len(set(blockReturnStatementTypes) - set(returnStatementTypes)) == 0:
                return returnStatementTypes[0]
            else:
                raise SemanticError(
                    "typ zwracany przez funkcje jest rozny od typu zwracanego przez blok"
                )
        elif len(set(returnStatementTypes)) == 0:
            returnStatementTypes.append(None)
            if len(set(blockReturnStatementTypes) - set(returnStatementTypes)) == 0:
                return None
            else:
                raise SemanticError(
                    "typ zwracany przez funkcje jest rozny od typu zwracanego przez blok"
                )
        else:
            raise SemanticError(
                "rozne zwracane typy w bloku "
            )

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

        returnType = []
        self.visit(node.condition)
        parentScope = self.executionScope.getParentScope()
        currentScope = self.executionScope.getCurrentScope()

        self.executionScope = ExecutionScope(parentScope + currentScope, Scope([], []))

        returnType.append(self.visit(node.content))

        if node.elseBlock:
            returnType.append(self.visit(node.elseBlock))

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
