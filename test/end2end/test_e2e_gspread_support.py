# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

import unittest
import os
import json
from support import gspread_support


# +
class Test_System_GoogleSheets_Connector(unittest.TestCase):


    def test_get_components_from_jira(self):
        gs = gspread_support.get_gspread()
        sh = gs.open("Recon Tools Test Data")
        cell = sh.sheet1.cell(1,1).value
        self.assertEqual("Test Data...", cell)

#    def test_get_raw_data(self):
#        expected = [['A1', 'B1', 'C1'], ['A2', '', ''], ['', 'B3', '']]
        #gs = gspread_support.get_gspread()
        #sh = gs.open("Recon Tools Test Data").sheet1
        #sh.worksheet(sheet_name).update(start_ref, data_in)

        #self.assertEqual(expected, all_cells)
        #print(all_cells)
# -







# %run test_e2e_gspread_support.py

if __name__ == '__main__':
    unittest.main()
