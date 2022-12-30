import unittest
import os
from transform import data_translations as dt
import pandas as pd
import numpy as np


class Test_Unit_Data_Translations(unittest.TestCase):

    def test_get_raw_data(self):
        sheet_data = [[0, 'Time Stamp', 'id', 'name', 'owner', 'description'], [1, '2021-09-26T21:09:21+02:00', '10000', 'TestComponent1', '<No Owner>', 'TestComponent1 Description'], [2, '2021-09-26T21:09:21+02:00', '999', '', '', ''], [3, '2021-09-26T21:09:21+02:00', '10002', 'TestComponent3', '', 'TestComponent3 Description'], [4, '2021-09-26T21:09:21+02:00', '10003', 'SHOULD BE DELETED', '', 'SHOULD BE DELETED']]
        self.assertEqual("test_first_data_translations", dt.test_first())

    def test_make_first_row_header(self):
        sample_data = [['id', 'b'], [1, 1], [2, 3]]
        df = pd.DataFrame(sample_data)

        dt.print_debug(df)
        df = dt.make_first_row_header(df)

    def test_process_component_sheets_data(self):
        sample_data = [[0, 1, 1], ['time', 'id', 'b'], [0, 1, 1], [0, 2, 3], [0, 2, 3], [0, 2, 3]]
        df = pd.DataFrame(sample_data)
        dt.print_debug(df)
        df = dt.process_component_sheets_data(df)
        dt.print_debug(df)




if __name__ == '__main__':
    unittest.main()
