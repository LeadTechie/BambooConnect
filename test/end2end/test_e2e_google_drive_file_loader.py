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
    os.chdir("../..")
    try:
        import support.authentication_support as auth_support
        from loaders.google_drive_file_loader import Google_Drive_File_Loader
        #from connectors.googlesheets_connector import GoogleSheets_Connector
    except Exception as e:
        print(e)
    finally:
        print("Finally - returning to project dir")
        os.chdir("./test/end2end")
    print("Imported Jupyter Version")
else:
    #Assumes script running from main project directory
    import support.authentication_support as auth_support
    from loaders.google_drive_file_loader import Google_Drive_File_Loader
    print("Imported Non Jupyter Version")
# -



class Test_Google_Drive_File_Loader(unittest.TestCase):

    def test_Google_Drive_Loader(self):
        expected = "hello, first file saved!"

        parameters = {
            "folder_id": "1dM-9RcAtT3IRlV_McL7Dw-y1hT5it7Pl",
            "file_name": "Google_Drive_File_Loader_savefile.txt",
            "credentials_json": auth_support.decode_credentials_json()
        }
        gdfl = Google_Drive_File_Loader(parameters,"../test_data")
        file_content = gdfl.save_data("hello, first file saved!")
        self.assertEqual(file_content, expected, "Content should be saved to Google Drive")

        #get_file_by_name: Google_Drive_File_Loader_savefile.txt


# +
#unittest.main()
# -

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)
