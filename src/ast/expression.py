from .node import Node

class Expression(Node):
    def __init__(self, leftOperand, operation=None, rightOperand=None, line=None, column=None):
        super().__init__(line, column)
        self.leftOperand = leftOperand
        self.operation = operation
        self.rightOperand = rightOperand

    def __eq__(self, other):
        return self.leftOperand == other.left_operand and self.operation == other.operation and self.rightOperand == other.rightOperand

    def __repr__(self):
        return f"[Expression: {self.leftOperand}, {self.operation}, {self.rightOperand}]"