def checkIfFuncArgumentsEqual(argumentsList,
                              otherArgumentsList):  # sprawdzanie czy lista argumentow jest taka sama
    if len(argumentsList) != len(otherArgumentsList):
        return False
    else:
        isEqual = True
        for i in range(len(argumentsList)):
            if argumentsList[i].varType != otherArgumentsList[i].varType:
                isEqual = False
                break
        return isEqual
