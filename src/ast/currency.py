from src.Token import TokenType, Characters
from src.ast.node import Node


class Currency(Node):
    def __init__(self,  varType, varId,  value =None, line=None, column=None):
        super().__init__(line, column)
        self.value = value
        self.varType = varType #currencyId definiuje typ zmiennej walutowej
        self.varId = varId
    def __repr__(self):
        return f"(Currency:{self.varType}, {self.varId}, {self.value})"

    def __eq__(self, other):
        print("tu")
        print(self.value)
        print(other.value)
        return self.value == other.value and self.varType == other.varType and self.varId == other.varId

    def getChildren(self):
        return [self.varType, self.varId, self.value]

    def getType(self):
        return self.varType


