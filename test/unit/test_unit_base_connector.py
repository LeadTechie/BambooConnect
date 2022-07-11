import unittest
import os
from connectors.base_connector import Base_Connector


class Test_Unit_Base_Connector(unittest.TestCase):

    def test_get_raw_data(self):
        bc = Base_Connector()
        self.assertEqual(bc.get_raw_data(),[])

if __name__ == '__main__':
    unittest.main()
