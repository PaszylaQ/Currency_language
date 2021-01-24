from src.ast.node import Node


class Variable(Node):
    def __init__(self, varType, varId, value = None, line = None, column = None):
        super().__init__(line,column)
        self.varType = varType
        self.varId = varId
        self.value = value

    def __eq__(self, other):
        return self.varType == other.varType and self.varId == other.varId and self.value == other.value

    def __repr__(self):
        return f"(Variable: {self.varType}, {self.varId}, {self.value})"

    def setValue(self,value):
        self.value = value

    def getType(self):
        return self.varType

    def getChildren(self):
        result = []
        if self.varType:
            result.append(self.varType)
        if self.varId:
            result.append(self.varId)
        if self.value:
            result.append(self.value)
        return result
