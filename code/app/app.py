import pandas as pd
import os
import config
import constants
import utils
import transaction
from oauth2client import file
from fetch import fetch

""" Initial set up for testing. Will replace one the correlation is finished."""

imp_name = config.CONFIG["imp"]
exp_name = config.CONFIG["exp"]
store = file.Storage('fetch/credentials.json')

""" Setting up helper functions. """
utils = utils.Utils()
cross_correlate = utils.cross_correlate

"""Getting Data from Google"""


# exp = utils.get_sheet(constants, exp_name, fetch, file)
imp = utils.get_sheet(constants, imp_name, fetch, file)
exp = utils.get_sheet(constants, exp_name, fetch, file)
try:
    imp1 = pd.read_csv("/Users/xavierprospero/Desktop/CFAR/coding code/test/{}"
        .format("test_coding_imp - orders_from_20180601_to_20181130_20181204_1015.csv"))
except FileNotFoundError:
    print('file {} could not be found :('.format(imp_name))
try:
    exp1 = pd.read_csv("/Users/xavierprospero/Desktop/CFAR/coding code/test/{}"
        .format("test_coding_exp - Statement of Activity Detail.csv"))
except FileNotFoundError:
    print('file {} could not be found :('.format(exp_name))

"""Renaming the columns"""
print("local", imp1)
exp.columns = list(exp.iloc[constants.EXP_NAME_ROW])
print("pulled", imp)

"""Correlating all the data on the amazon sheet and creating a
    dictionary of all of the orders.
"""
amazon_rows = {}

for i in range(exp.shape[0]):
    row = exp.iloc[i]
    if "Amazon" in str(row["Name"]):
        date = row["Date"]
        amount = "$"+row["Amount"].strip()
        correlation = cross_correlate(amount, date, imp)
        indices = [idx for idx in range(len(correlation)) if correlation[idx] == 2]
        if not indices:
            amazon_rows.update({i: transaction.Transaction(False, ["Transaction not found"])})
        else:
            at_bodega = utils.check_bodega(imp.iloc[indices[0]])
            items = utils.get_items(indices, imp)
            amazon_rows.update({i: transaction.Transaction(at_bodega, items)})



""" Putting the data back on the sheet. """
# checking to see if this works.

for row in amazon_rows:
    if amazon_rows[row].get_bodega() == True:
        exp.at[row, utils.LOCATION] = "Bodega Bay"
        #Tested
    exp.at[row, utils.DESCRIPTION] = amazon_rows[row].get_items()

# print(exp.iloc[:, 7])

exp.to_csv(path+"/test_csv.csv")
