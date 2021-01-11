class Source:
    def __init__(self, filename):

        self.file = open(filename, 'r')
        self.positionInline = 0
        self.lineNumber = 0
        self.currentChar = self.nextChar()


    def getPositionInLine(self):
        return self.positionInline

    def getLineNumber(self):
        return self.lineNumber

    def getCurrentChar(self):
        return self.currentChar

    def readCharacter(self):
        return self.file.read(1)

    def nextChar(self):
        self.currentChar = self.readCharacter()
        if self.currentChar == '#':
            while self.currentChar != '\n' and self.currentChar !="":
                self.currentChar = self.readCharacter()
        if self.currentChar == '\n':
            self.positionInline = 0
            self.lineNumber += 1
        else:
            self.positionInline += 1
        return self.currentChar


