from src.NodeVisitor import NodeVisitor


class Interpreter(NodeVisitor):

    def __init__(self, tree):
        self.tree = tree

    def interpret(self):
        if self.tree is not None:
            for node in self.tree:
                self.visit(node)
        return ''

    def visitCurrency(self, node):
        pass

    def visitFunc(self, node):
        pass

    def visitFuncCall(self, node):
        pass
