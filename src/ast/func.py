from .node import Node


class Func(Node):
    def __init__(self, funcType ,  funcId, arguments, body = None, line=None, column=None):
        super().__init__(line ,column)
        self.funcType = funcType
        self.funcId = funcId
        self.arguments = arguments
        self.body = body

    def __eq__(self, other):
        return self.funcType == other.funcType and self.funcId == other.funcId and self.arguments == other.arguments and self.body == other.body

    def __repr__(self):
        return f"(Function: {self.funcType} {self.funcId}, {self.arguments}, {self.body})"

    def getChildren(self):
        return [self.funcId , self.arguments , self.body]

