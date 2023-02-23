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

# # !pip uninstall bamboo_connect -y


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
        from extractors.google_drive_file_extractor import Google_Drive_File_Extractor
        #from connectors.googlesheets_connector import GoogleSheets_Connector
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
    import Google_Drive_File_Loader
    print("Imported Non Jupyter Version")
# -



# +
class Test_Google_Drive_File_Extractor(unittest.TestCase):

    def test_Google_Drive_Extractor(self):
        expected = "hello, first file saved!"

        #https://drive.google.com/file/d/1rAVjKMKPSytsOfFzZsCpOk2l2OaN25em/view?usp=share_link        
        
        parameters = {
            "folder_id": "1dM-9RcAtT3IRlV_McL7Dw-y1hT5it7Pl",
            "file_name": "Google_Drive_File_Loader_savefile.txt",
            "credentials_json": auth_support.decode_credentials_json()
        }
        gdfe = Google_Drive_File_Extractor(parameters,"../test_data")
        print("set gdfe")
        file_content = gdfe.extract_data()
        print("file_content")
        print(file_content)
        self.assertEqual(file_content, expected, "Content should be loaded from Google Drive")

        #get_file_by_name: Google_Drive_File_Loader_savefile.txt
            
            
        
#logging.basicConfig(filename='debug.log', level=logging.DEBUG)
#logging.basicConfig(filename='debug.log', level=logging.DEBUG)
#unittest.main(argv=[''], verbosity=2, exit=False) 

# +
#unittest.main()
# -

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)
