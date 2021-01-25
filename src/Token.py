from enum import Enum, auto


class TokenType(Enum):
    NUMBER = auto()
    STRING = auto()
    NAME = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
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
    EOF = auto()
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
    BOOL = auto()
    BOOL_KW = auto()
    PLN_KW = auto()
    USD_KW = auto()
    GBP_KW = auto()
    CHF_KW = auto()
    AUD_KW = auto()
    EUR_KW = auto()
    CZK_KW = auto()
    RUB_KW = auto()
    JPY_KW = auto()
    DOUBLE_QUOTE = auto()


class Characters:
    keywords = {

        'def': TokenType.DEF_KW,
        'print': TokenType.PRINT_KW,
        'var': TokenType.VAR_KW,
        'while': TokenType.WHILE_KW,
        'if': TokenType.IF_KW,
        'else': TokenType.ELSE_KW,
        'return': TokenType.RETURN_KW,
        'string': TokenType.STRING,
        'true': TokenType.BOOL,
        'false': TokenType.BOOL,
        'bool': TokenType.BOOL_KW,
        'PLN': TokenType.PLN_KW,
        'USD': TokenType.USD_KW,
        'GBP': TokenType.GBP_KW,
        'CHF': TokenType.CHF_KW,
        'AUD': TokenType.AUD_KW,
        'EUR': TokenType.EUR_KW,
        'CZK': TokenType.CZK_KW,
        'RUB': TokenType.RUB_KW,
        'JPY': TokenType.JPY_KW
    }

    characters = {
        '+': TokenType.PLUS,
        '-': TokenType.MINUS,
        '*': TokenType.MULTIPLY,
        '/': TokenType.DIVIDE,
        '!': TokenType.NOT,
        '>': TokenType.GREATER,
        '<': TokenType.LESS,
        '&': TokenType.AND,
        '|': TokenType.OR,
        '[': TokenType.LEFTBRACKET,
        ']': TokenType.RIGHTBRACKET,
        '(': TokenType.LEFTPARENTHESIS,
        ')': TokenType.RIGHTPRAENTHESIS,
        '{': TokenType.LEFTCURLY,
        '}': TokenType.RIGHTCURLY,
        ',': TokenType.COMMA,
        '=': TokenType.ASSIGN,
        ';': TokenType.SEMICOLON,
        ':': TokenType.COLON,
        '.': TokenType.DOT,
        '"': TokenType.DOUBLE_QUOTE

    }

    doubleOperators = {
        '==': TokenType.EQUALS,
        '!=': TokenType.NOTEQUAL,
        '>=': TokenType.GREATEROREQUAL,
        '<=': TokenType.LESSOREQUAL
    }
    currencies = {
        'PLN': TokenType.PLN_KW,
        'USD': TokenType.USD_KW,
        'GBP': TokenType.GBP_KW,
        'CHF': TokenType.CHF_KW,
        'AUD': TokenType.AUD_KW,
        'EUR': TokenType.EUR_KW,
        'CZK': TokenType.CZK_KW,
        'RUB': TokenType.RUB_KW,
        'JPY': TokenType.JPY_KW
    }
    def currencyTypesToList(self):
        currencyList = []
        for i in range(len(self.currencies)):
            currencyList.append(list(self.currencies.values())[i])
        return currencyList



class Token:

    def __init__(self, tokenType=TokenType.UNKNOWN, value="", line = None, column = None):
        self.tokenType = tokenType
        self.value = value
        self.line = line
        self.column = column

    def getValue(self):
        return self.value

    def getType(self):
        return self.tokenType

    def __repr__(self):
        return f"[Token: {self.tokenType}, {self.value}]"

    def get_position(self):
        return self.line, self.column
