import unittest
import os
import json
from connectors.googlesheets_connector import GoogleSheets_Connector


class Test_System_GoogleSheets_Connector(unittest.TestCase):


    def test_get_components_from_jira(self):
        gsc = GoogleSheets_Connector()
        gsc.initialse_auth()
        cell = gsc.get_cell("Recon Tools Test Data","A1")
        self.assertEqual([['2021-09-26T21:09:21+02:00']], cell)

    def test_get_raw_data(self):
        expected = [['A1', 'B1', 'C1'], ['A2', '', ''], ['', 'B3', '']]
        gsc = GoogleSheets_Connector()
        gsc.initialse_auth()
        all_cells= gsc.get_raw_data("Recon Tools Test Data", "Sheet3")
        self.assertEqual(expected, all_cells)
        #print(all_cells)



if __name__ == '__main__':
    unittest.main()
