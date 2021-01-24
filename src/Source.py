import sys


class Source:
    def __init__(self):

        self.positionInline = 0
        self.lineNumber = 1
        self.currentChar = self.nextChar()

    def getCurrencies(self, filepath):
        file = open(filepath, "r")

    def getPositionInLine(self):
        return self.positionInline

    def getLineNumber(self):
        return self.lineNumber

    def getCurrentChar(self):
        return self.currentChar

    def readCharacter(self):
        return sys.stdin.read(1)

    def nextChar(self):
        self.currentChar = self.readCharacter()
        if self.currentChar == '#':
            while self.currentChar != '\n' and self.currentChar != "":
                self.currentChar = self.readCharacter()
        if self.currentChar == '\n':
            self.positionInline = 0
            self.lineNumber += 1
        else:
            self.positionInline += 1
        return self.currentChar
