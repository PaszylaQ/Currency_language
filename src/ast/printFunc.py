from .node import Node

class PrintFunc(Node):
    def __init__(self, identifier, line=None, column=None):
        super().__init__(line, column)
        self.identifier = identifier

    def __eq__(self, other):
        return self.identifier == other.identifier

    def __repr__(self):
        return f"[PRINT: {self.identifier}]"