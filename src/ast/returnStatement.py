from .node import Node

class ReturnStatement(Node):
    def __init__(self, leftOperand, operation=None, rightOperand=None, line=None, column=None):
        super().__init__(line, column)
        self.leftOperand = leftOperand
        self.operation = operation
        self.rightOperand = rightOperand

    def __eq__(self, other):
        return self.leftOperand == other.leftOperand and self.operation == other.operation and self.rightOperand == other.rightOperand

    def __repr__(self):
        return f"(ReturnStatement: {self.leftOperand}, {self.operation}, {self.rightOperand})"

    def getChildren(self):
        result = []
        if self.leftOperand:
            result.append(self.leftOperand)
        if self.operation:
            result.append(self.operation)
        if self.rightOperand:
            result.append(self.rightOperand)
        return result
