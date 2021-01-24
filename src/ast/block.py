from src.ast.node import Node


class Block(Node):

    def __init__(self, listOfStatements=[], returnStatement=None, line=None, column=None):
        super().__init__(line, column)
        self.listOfStatements = listOfStatements
        self.returnStatement = returnStatement

    def __repr__(self):
        return f"(Block: {self.listOfStatements}, {self.returnStatement})"

    def __eq__(self, other):
        return self.listOfStatements == other.listOfStatements and self.returnStatement == other.returnStatement

    def getChildren(self):
        results = []
        if self.listOfStatements:
            results.append(self.listOfStatements)
        if self.returnStatement:
            results.append(self.returnStatement)
        return results
