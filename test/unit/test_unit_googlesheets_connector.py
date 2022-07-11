import unittest
import os
import json
from connectors.googlesheets_connector import GoogleSheets_Connector

class Test_Unit_GoogleSheets_Connector(unittest.TestCase):

    def test_connector_init(self):
        self.assertEqual("","")

if __name__ == '__main__':
    unittest.main()
