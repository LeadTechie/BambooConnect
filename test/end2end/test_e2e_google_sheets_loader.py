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



# +
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
    os.chdir("../..")
    print(os.getcwd())
    try:
        import support.authentication_support as auth_support
        from loaders.google_sheets_loader import Google_Sheets_Loader
    except Exception as e:
        print(e)
    finally:
        print("Finally - returning to project dir")
        print(os.getcwd())
        os.chdir("./test/end2end/")
        print(os.getcwd())
    print("Imported Jupyter Version")
else:
    #Assumes script running from main project directory
    import support.authentication_support as auth_support
    from loaders.google_sheets_loader import Google_Sheets_Loader
    print("Imported Non Jupyter Version")


# +
class Test_Google_Sheets_Loader(unittest.TestCase):

    def test_Google_Sheets_Loader(self):
        data_to_save = [['Bamboo Test E1', 'Bamboo Test F1'],
                        ['Bamboo Test E2', 'Bamboo Test F2']]

        parameters = {
            "file_id": "12keD9VYi6yrQ4nP7JJh95M8lmyTqIJw-V4IocOcyjYM",
            "tab_name": "Sheet1",
            "data_range": "E1:F2",
            "credentials_json": auth_support.decode_credentials_json()
        }
        gdse = Google_Sheets_Loader(parameters,"../test_data")
        result = gdse.save_data(data_to_save)
        expected = ""
        self.assertEqual(result['updatedCells'], 4, "It should return that 4 cells were updated")


#logging.basicConfig(level=logging.ERROR)

# +


if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)

