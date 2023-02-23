#!/usr/bin/env python
# coding: utf-8
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



# +


import unittest
import os
import logging


# +


# !pip install gspread

# Relative import work around if running interactively in Jupyter
def running_in_jupyter():
    try:
        get_ipython()
        return True
    except NameError:
        return False

if running_in_jupyter():
    # Go up two levels, import class then return to original subdirectory
    print(os.getcwd())
    os.chdir("../../samples")
    print(os.getcwd())
    try:
        import poc_e2e_script as poc_e2e
    except Exception as e:
        print(e)
    finally:
        print("Finally - returning to project dir")
        print(os.getcwd())
        os.chdir("../test/end2end")
    print(os.getcwd())
    print("Imported Jupyter Version")
else:
    #Assumes script running from main project directory
    import poc_e2e_script as poc_e2e
    print("Imported Non Jupyter Version")


# +


class Test_e2e_poc_recon(unittest.TestCase):

    def test_e2e_poc_recon(self):
        clean_data = poc_e2e.read_clean_test_data()
        poc_e2e.write_clean_test_data(clean_data.values.tolist())
        poc_e2e.load_jira_and_google_data_and_reconcile_and_save_results()
        actual = poc_e2e.read_clean_test_expected_results("Sheet1")
        expected = poc_e2e.read_clean_test_expected_results("ExpectedResult")

        self.assertEquals(actual.values.tolist(), expected.values.tolist(), "Check that after reconciliation the results match the expected")




# +


if __name__ == '__main__':
    #logging.basicConfig(level=logging.ERROR)
    unittest.main(argv=[''], verbosity=2, exit=False)    

