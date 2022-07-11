import unittest
import os

class Test_Integration_QuickTest(unittest.TestCase):

    def test_get_raw_data(self):
        self.assertEqual("sample integration test","sample integration test")


if __name__ == '__main__':
    unittest.main()
