from .node import Node
from ..Token import TokenType


class Name(Node):
    def __init__(self, name, line=None, column=None):
        super().__init__(line, column)
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return f"(Identifier: {self.name})"

    def getChildren(self):
        return self.name

    def getType(self):
        return TokenType.NAME