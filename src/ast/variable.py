from src.ast.node import Node


class Variable(Node):
    def __init__(self, var_type, var_id, value = None, line = None, column = None):
        super().__init__(line,column)
        self.var_type = var_type
        self.var_id = var_id
        self.value = value

    def __eq__(self, other):
        self.var_type == other.var_type and self.var_id == other.var_id and self.value == other.value

    def __repr__(self):
        return f"[Variable: {self.var_type}, {self.var_id}, {self.value}]"