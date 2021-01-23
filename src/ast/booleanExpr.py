from .node import Node

class BooleanExpr(Node):

    def __init__(self,lValue, operator, rValue, line=None, column=None):
        super().__init__(line, column)
        self.lValue = lValue
        self.rValue = rValue
        self.operator = operator


    def __repr__(self):
        return f"(BooleanExpr: {self.lValue},{self.operator}, {self.rValue})"

    def __eq__(self, other):
        return self.lValue == other.lValue and self.operator == other.operator and self.rValue == other.rValue

    def getChildren(self):
        return [self.lValue, self.operator, self.rValue]