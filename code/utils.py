""" Basic utils for app. """

class Utils:

    """Constants for correlation"""
    DATE = "Payment Date"
    AMOUNT = "Payment Amount"

    """Constants for Item extraction"""
    BODEGA = "Shipping Address"
    ITEM = "Title"
    LOCATION = "Location"
    DESCRIPTION = "Memo/Description"

    def correlate(self, price, date, row):
        d = 1 if price == row[self.AMOUNT] else 0
        a = 1 if date == row[self.DATE] else 0
        return a + d

    def cross_correlate(self, price, date, imp):
        correlations = [None] * imp.shape[0]
        for i in range(imp.shape[0]):
            correlations[i] = self.correlate(price, date, imp.iloc[i])
        return correlations


    """Check to see if this order was made to Bodega Bay"""
    def check_bodega(self, row):
        return "Bodega Bay" in row[self.BODEGA]

    def get_items(self, rows, imp):
        values = []
        for i in rows:
            values.append(imp.iloc[i][self.ITEM])
        return values

    """Save files to folder as csv."""
    def save_df(self, df, path):
        #working
