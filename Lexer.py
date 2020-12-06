import sys

import ply.lex as lex


class Lexer(object):
    if len(sys.argv) == 2:
        filePath = sys.argv[1]
    else:
        filePath = "/Users/maciekpaszylka/Desktop/test.txt"

    # List of token names.   This is always required
    def __init__(self):
        self.data =[]
        self._tokens=[]

    tokens = (
        'NUMBER',
        'STRING',
        'NAME',
        'PLUS',
        'MINUS',
        'MULTIPLY',
        'DIVIDE',
        'ASSIGN',
        'EQUALS',
        'NOTEQUAL',
        'GREATEROREQUAL',
        'LESSOREQUAL',
        'GREATER',
        'LESS',
        'AND',
        'OR',
        'LEFTBRACKET',
        'RIGHTBRACKET',
        'LEFTPARENTHESIS',
        'RIGHTPRAENTHESIS',
        'LEFTCURLY',
        'RIGHTCURLY',
        'COMMA',
        'EOL'

    )

    # Regular expression rules for simple tokens
    t_STRING = r'\".*?\"'
    t_PLUS = r'\+'
    t_MINUS = r'\-'
    t_MULTIPLY = r'\*'
    t_DIVIDE = r'\/'
    t_ASSIGN = r'\='
    t_EQUALS = r'\=='
    t_NOTEQUAL = r'\!='
    t_GREATEROREQUAL = r'\>='
    t_LESSOREQUAL = r'\<='
    t_GREATER = r'\>'
    t_LESS = r'\<'
    t_AND = r'\&'
    t_OR = r'\|'
    t_LEFTBRACKET = r'\['
    t_RIGHTBRACKET = r'\]'
    t_LEFTPARENTHESIS = r'\('
    t_RIGHTPRAENTHESIS = r'\)'
    t_LEFTCURLY = r'\{'
    t_RIGHTCURLY = r'\}'
    t_COMMA = r'\,'
    t_EOL = r'\;'

    keywords = {

        'def': 'DEF',
        'print': 'PRINT',
        'var': 'VAR',
        'while': "WHILE",
        'if': "IF",
        'else': 'ELSE'
    }

    tokens += tuple(keywords.values())

    def t_NUMBER(self, t):
        r'(\d+(?:\.\d+)?)'
        t.value = float(t.value)
        return t

    def t_NAME(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.keywords.get(t.value, 'NAME')
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    t_ignore = ' \t'

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def tokenize_input(self, filePath):
        filePath = self.filePath
        with open(filePath, 'r') as f:
            self.data = f.readlines()
        for line in self.data:
            for c in line.split():
                self.tokenize(c)
        return self._tokens


    def tokenize(self, data):

        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break;
            self._tokens.append(tok)
            return tok


m = Lexer()
m.build()

data = m.tokenize_input(m.filePath)
for dat in data:
    print(dat)
