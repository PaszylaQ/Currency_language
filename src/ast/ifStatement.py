from .node import Node


class IfStatement(Node):
    def __init__(self, condition, content, elseBlock = None, line=None, column=None):
        super().__init__(line, column)
        self.content = content
        self.condition = condition
        self.elseBlock = elseBlock


    def __repr__(self):
        return f"[IfStatement: {self.condition}, {self.content}, {self.elseBlock}]"