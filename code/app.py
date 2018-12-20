import pandas as pd
import os
import config
import constants
import utils
import transaction

""" Initial set up for testing. Will replace one the correlation is finished."""

path = config.CONFIG["test_path"]
imp_name = config.CONFIG["imp"]
exp_name = config.CONFIG["exp"]

""" Setting up helper functions. """
utils = utils.Utils()
cross_correlate = utils.cross_correlate

try:
    imp = pd.read_csv(path.strip() + "/{}".format(imp_name))
except FileNotFoundError:
    print('file {} could not be found :('.format(imp_name))
try:
    exp = pd.read_csv(path.strip() + "/{}".format(exp_name))
except FileNotFoundError:
    print('file {} could not be found :('.format(exp_name))

"""Renaming the columns"""
exp.columns = list(exp.iloc[constants.EXP_NAME_ROW])

"""Correlating all the data on the amazon sheet and creating a
    dictionary of all of the orders.
"""
amazon_rows = {}
print(exp)
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
