from src.Source import Source
from src.Token import TokenType, Token, Characters


class Lexer:

    def __init__(self, source: Source):
        self.source = source
        self.token = Token()

    def skipWhitespace(self):
        while self.source.getCurrentChar() == " " or self.source.getCurrentChar() == "\n":
            self.source.nextChar()

    def readName(self):
        currentChar = self.source.getCurrentChar()
        name = ""
        if currentChar.isalpha():
            while currentChar.isalpha() or currentChar.isdigit():
                name+=currentChar
                currentChar = self.source.nextChar()
        return name

    def readString(self):
        currentChar = self.source.getCurrentChar()
        buffer = None
        if currentChar == '"':
            buffer = ""
            currentChar= self.source.nextChar()
            while currentChar != '"':
                if currentChar == '':
                    print("Unterminated string")
                    break
                else:
                    buffer+=currentChar
                    currentChar = self.source.nextChar()
        return buffer


    def checkText(self):
        text = self.readString()
        if text != None:
            self.token = Token(TokenType.TEXT, text)
            self.source.nextChar()
            return True
        return False

    def readNumber(self):
        currentChar = self.source.getCurrentChar()
        number = ""

        if currentChar == '0':
            number += currentChar
            currentChar = self.source.nextChar()

        elif currentChar.isdigit() and currentChar != 0:
            while currentChar.isdigit() or currentChar =='.':

                number+= currentChar
                currentChar = self.source.nextChar()
        return number

    def checkCharacter(self):
        currentChar = self.source.getCurrentChar()
        if currentChar in Characters.characters:
            tokenType = Characters.characters[currentChar]
            self.token = Token(tokenType, currentChar)
            self.source.nextChar()
            return True
        return False

    def checkIfDoubleOperator(self):
        currentChar = self.source.getCurrentChar()
        operators = ""
        if currentChar == '>' or currentChar== '<' or currentChar == '=' or currentChar =='!':
            operators += currentChar
            currentChar = self.source.nextChar()
            if(operators+currentChar) in Characters.doubleOperators:
                tokenType = Characters.doubleOperators[operators+currentChar]
                self.token = Token(tokenType, operators+currentChar)
                self.source.nextChar()
                return True
            elif operators in Characters.characters:
                tokenType = Characters.characters[operators]
                self.token = Token(tokenType, operators)
                self.source.nextChar()
                return True
        return False

    def checkIfKeyword(self):
        keyword = self.readName()
        if keyword in Characters.keywords:
            token_type = Characters.keywords[keyword]
            self.token = Token(token_type, keyword)
            return True
        elif keyword != "":
            self.token = Token(TokenType.NAME, keyword)
            return True
        return False

    def checkIfNumber(self):
        number = self.readNumber()
        if number != "":
            self.token = Token(TokenType.NUMBER, number)
            return True
        return False

    def checkIfEof(self):
        currentChar = self.source.getCurrentChar()
        if currentChar == "":
            self.token = Token(TokenType.EOF, None)
            return True
        return False


    def tokenize(self):
        self.skipWhitespace()
        if self.checkIfEof():
            return
        elif self.checkIfKeyword():
            return
        elif self.checkIfNumber():
            return
        elif self.checkText():
            return
        elif self.checkIfDoubleOperator():
            return
        elif self.checkCharacter():
            return
        else:
            self.token = Token(TokenType.UNKNOWN, self.source.getCurrentChar())
            self.source.nextChar()
            return

    def getToken(self):
        return self.token


#lexer = Lexer("/Users/maciekpaszylka/Desktop/test2.txt")

# lexer = Lexer("testText.txt")

# #while lexer.getToken().getType() != TokenType.EOL:
# lexer.tokenize()
# print(lexer.getToken())
