import unittest
import os
from recon_dataset import Recon_DataSet


class Test_Unit_Recon_DataSet(unittest.TestCase):

    def test_get_raw_data(self):
        rds = Recon_DataSet()
        self.assertEqual("test_first", rds.test_first())

if __name__ == '__main__':
    unittest.main()
