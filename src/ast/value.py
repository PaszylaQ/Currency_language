from src.ast.node import Node


class Value(Node):
    def __init__(self, value, line=None, column=None):
        super().__init__(line, column)
        self.value = value

    def __repr__(self):
        return f"(Value: {self.value})"

    def __eq__(self, other):
        return self.value == other.value

    def accept(self, visitor):
        return visitor.visit_value(self)

    def getChildren(self):
        return self.value
