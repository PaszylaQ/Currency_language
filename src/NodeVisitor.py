class NodeVisitor:
    def visit(self, node, exchangeRate = None ):
        method_name = 'visit' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return   visitor(node, exchangeRate) if exchangeRate else visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit{} method'.format(type(node).__name__))
