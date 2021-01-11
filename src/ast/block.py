from src.ast.node import Node


class Block(Node):

    def __init__(self, listOfStatements = [], returnStatement = None, line = None, column = None):
        super().__init__(line,column)
        self.listOfStatements = listOfStatements
        self.returnStatement = returnStatement

    def __repr__(self):
        return f"[Assignement: {self.listOfStatements}, {self.returnStatement}]"