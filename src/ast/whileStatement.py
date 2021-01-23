from .node import Node


class WhileStatement(Node):
    def __init__(self, condition, content, line=None, column=None):
        super().__init__(line, column)
        self.content = content
        self.condition = condition


    def __repr__(self):
        return f"(WhileStatement: {self.condition}, {self.content})"

    def __eq__(self, other):
        return self.condition == other.condition and self.content == other.content

    def getChildren(self):
        return [self.condition, self.content]