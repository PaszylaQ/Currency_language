from src.utils.checkIfFuncArgumentsEqual import checkIfFuncArgumentsEqual


class Scope():
    def __init__(self, variables, functions):
        self.variables = variables
        self.functions = functions

    def __repr__(self):
        return f"[Scope: {self.getVarIds(self.variables)}  {self.getVarValue(self.variables)}'\n' {self.getFuncIds(self.functions)}]"

    def getVarIds(self, variables):
        vars = []
        for variable in variables:
            vars.append(variable.varId)
        return vars

    def getVarValue(self, variables):
        vars = []
        for variable in variables:
            vars.append(variable.value)
        return vars

    def getFuncIds(self, functions):
        funcs = []
        for func in functions:
            funcs.append(func.funcId)
        return funcs

    def pushVarDeclaration(self, variable):
        self.variables.append(variable)

    def pushFuncDeclaration(self, function):
        self.functions.append(function)

    def checkIfVarDeclared(self, variable):
        temp = False
        for id in self.variables:
            temp = id.varId == variable.varId
        return temp

    def checkIfFuncDeclared(self, function):
        temp = False
        for func in self.functions:
            temp = func.funcId == function.funcId and checkIfFuncArgumentsEqual(function.arguments, func.arguments)
        return temp

    def __add__(self, other):
        return Scope(self.variables + other.variables, self.functions + other.functions)


class ExecutionScope():

    def __init__(self, parentScope, currentScope):
        self.parentScope = parentScope
        self.currentScope = currentScope

    def lookupVariable(self, variable, currentScopeOnly=False):
        temp = False
        if currentScopeOnly != True:
            temp = self.parentScope.checkIfVarDeclared(variable)
        return self.currentScope.checkIfVarDeclared(variable) or temp

    def lookupFunction(self, function, currentScopeOnly=False):
        temp = False
        if currentScopeOnly != True:
            temp = self.parentScope.checkIfFuncDeclared(function)
        return self.currentScope.checkIfFuncDeclared(function) or temp

    def lookupVariableAndReturnVar(self, variableName, currentScopeOnly=False):

        for var in reversed(self.currentScope.variables):
            if var.varId == variableName:
                lookupVar = var
                return lookupVar  # sprawdzanie najepirw current a potem parent scope w przypadku nieodnalezienia

        if currentScopeOnly != True:
            for var in reversed(self.parentScope.variables):
                if var.varId == variableName:
                    lookupVar = var
                    return lookupVar

    def lookupAndReturnFunction(self, funcCall, currentScopeOnly=False):
        lookupFunc = None

        for func in reversed(self.currentScope.functions):
            if func.funcId == funcCall.funcId and checkIfFuncArgumentsEqual(funcCall.arguments, func.arguments):
                lookupFunc = func
                return lookupFunc  # sprawdzanie najepirw current a potem parent scope w przypadku nieodnalezienia

        if currentScopeOnly != True:
            for func in reversed(self.parentScope.functions):
                if func.funcId == funcCall.funcId and checkIfFuncArgumentsEqual(funcCall.arguments, func.arguments):
                    lookupFunc = func
                    return lookupFunc

    def pushVariables(self, variables):
        for variable in variables:
            self.pushVariable(variable)

    def pushVariable(self, variable):
        self.currentScope.pushVarDeclaration(variable)

    def pushFunction(self, function):
        self.currentScope.pushFuncDeclaration(function)

    def getCurrentScope(self):
        return self.currentScope

    def getParentScope(self):
        return self.parentScope

    def searchAndReplaceValue(self, id, value):

        for var in reversed(self.currentScope.variables):
            if var.varId == id:
                var.value = value
                return
                # sprawdzanie najepirw current a potem parent scope w przypadku nieodnalezienia
        for var in reversed(self.parentScope.variables):
            if var.varId == id:
                var.value = value
                return
#
# var savings = 2.0;
#
# def func(a, b, c){
#     var savings2 = 3.0
#     if(savings >3){
#     dosomething()
# }
#     current = savings, func, a, b , c
# }
# parent = []
# current(savings)
# new parent = current + parent
# current = [func,a,b,c, savings2]
#
# current (savings2)
