from src.Token import TokenType
from src.ast.value import Value


class Bool(Value):
    def __init__(self, value, line=None, column=None):
        self.line = line
        self.column = column
        super().__init__(value)

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        return f"(BOOL: {self.value})"

    def getChildren(self):
        return self.value

    def getType(self):
        return TokenType.BOOL_KW
