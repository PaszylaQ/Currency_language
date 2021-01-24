from .node import Node


class FuncCall(Node):
    def __init__(self, functionId, args = None, line=None, column=None):
        super().__init__(line, column)
        self.functionId = functionId
        self.args = args

    def __eq__(self, other):
        return self.functionId == other.functionId and self.args == other.args

    def __repr__(self):
        return f"(FuncCall: {self.functionId}, {self.args})"

    def getChildren(self):
        result = []
        if self.functionId:
            result.append(self.functionId)
        if self.args:
            result.append(self.args)
        return result