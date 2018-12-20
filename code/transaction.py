""" A single transaction.
    Types:
        bodega is bool
        items is a list of strings
"""

class Transaction:

    def __init__(self, bodega, items):
        self.bodega = bodega
        self.items = items

    def __repr__(self):
        return self.get_items() + str(self.get_bodega())

    def get_items(self):
        total = ""
        for i in self.items:
            total += i.split(", ")[0]+";"
        return total

    def get_bodega(self):
        return self.bodega
