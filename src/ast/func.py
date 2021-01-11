from .node import Node


class Func(Node):
    def __init__(self, funcId, arguments, body, line=None, column=None):
        super().__init__(line ,column)
        self.funcId = funcId
        self.arguments = arguments
        self.body = body

    def __eq__(self, other):
        return self.funcId == other.funcId and self.arguments == other.arguments and self.body == other.body

    def __repr__(self):
        return f"[Function: {self.funcId}, {self.arguments}, {self.body}]"