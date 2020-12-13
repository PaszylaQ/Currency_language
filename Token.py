from enum import Enum, auto


class TokenType(Enum):
    NUMBER = auto()
    STRING = auto()
    NAME = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY =auto()
    DIVIDE = auto()
    ASSIGN = auto()
    EQUALS = auto()
    NOTEQUAL = auto()
    NOT = auto()
    GREATEROREQUAL = auto()
    LESSOREQUAL = auto()
    GREATER = auto()
    LESS = auto()
    AND = auto()
    OR = auto()
    LEFTBRACKET = auto()
    RIGHTBRACKET = auto()
    LEFTPARENTHESIS = auto()
    RIGHTPRAENTHESIS = auto()
    LEFTCURLY = auto()
    RIGHTCURLY = auto()
    COMMA = auto()
    EOL = auto()
    UNKNOWN = auto()
    DEF_KW = auto()
    PRINT_KW = auto()
    VAR_KW = auto()
    WHILE_KW = auto()
    IF_KW = auto()
    ELSE_KW = auto()
    RETURN_KW = auto()
    COLON = auto()
    SEMICOLON = auto()
    DOT = auto()
    TEXT = auto()




class Characters:
    keywords = {

        'def': TokenType.DEF_KW,
        'print': TokenType.PRINT_KW,
        'var': TokenType.VAR_KW,
        'while': TokenType.WHILE_KW,
        'if': TokenType.IF_KW,
        'else': TokenType.ELSE_KW,
        'return': TokenType.RETURN_KW,
        'string': TokenType.STRING
    }

    characters = {
        '+' : TokenType.PLUS,
        '-' : TokenType.MINUS,
        '*' : TokenType.MULTIPLY,
        '/' : TokenType.DIVIDE,
        '!' : TokenType.NOT,
        '>' : TokenType.GREATER,
        '<' : TokenType.LESS,
        '&' : TokenType.AND,
        '|' : TokenType.OR,
        '[' : TokenType.LEFTBRACKET,
        ']' : TokenType.RIGHTBRACKET,
        '(' : TokenType.LEFTPARENTHESIS,
        ')' : TokenType.RIGHTPRAENTHESIS,
        '{' : TokenType.LEFTCURLY,
        '}' : TokenType.RIGHTCURLY,
        ',' : TokenType.COMMA,
        '=' : TokenType.ASSIGN,
        ';' : TokenType.SEMICOLON,
        ':' : TokenType.COLON,
        '.' : TokenType.DOT

    }

    doubleOperators={
        '==' : TokenType.EQUALS,
        '!=' : TokenType.NOTEQUAL,
        '>=' : TokenType.GREATEROREQUAL,
        '<=' : TokenType.LESSOREQUAL
    }

class Token:

    def __init__(self, tokenType = TokenType.UNKNOWN, value= ""):
        self.tokenType = tokenType
        self.value = value


    def getType(self):
        return self.tokenType

    def __repr__(self):
        return f"Typ tokenu : {self.tokenType}, value = '{self.value}'"