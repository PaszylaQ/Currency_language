from .node import Node


class Name(Node):
    def __init__(self, name, line=None, column=None):
        super().__init__(line, column)
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return f"[Identifier: {self.name}]"