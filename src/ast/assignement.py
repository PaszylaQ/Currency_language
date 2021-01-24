from src.ast.node import Node


class Assignement(Node):

    def __init__(self, name, expression, line=None, column=None):
        super().__init__(line, column)
        self.name = name
        self.expression = expression

    def __repr__(self):
        return f"(Assignement: {self.name}, {self.expression})"

    def __eq__(self, other):
        return self.name == other.name and self.expression == other.expression

    def getChildren(self):
        return [self.name, self.expression]
