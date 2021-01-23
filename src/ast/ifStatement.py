from .node import Node


class IfStatement(Node):
    def __init__(self, condition, content, elseBlock = None, line=None, column=None):
        super().__init__(line, column)
        self.content = content
        self.condition = condition
        self.elseBlock = elseBlock


    def __repr__(self):
        return f"(IfStatement: {self.condition}, {self.content}, {self.elseBlock})"

    def __eq__(self, other):
        return self.condition == other.condition and self.content == other.content and self.elseBlock == other.elseBlock

    def getChildren(self):
        result = []
        if self.condition:
            result.append(self.condition)
        if self.content:
            result.append(self.content)
        if self.elseBlock:
            result.append(self.elseBlock)
        return result