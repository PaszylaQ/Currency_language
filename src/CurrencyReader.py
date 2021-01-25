import json


class CurrencyReader():
    def __init__(self, filepath):
        self.filepath = filepath

    def getCurrencies(self):
        with open(self.filepath) as f:
            currencies = json.load(f)
        return currencies

    def getExchange(self, tokenType):
        currencies = self.getCurrencies()


#/Users/maciekpaszylka/PycharmProjects/Project_TKOM/src/utils
