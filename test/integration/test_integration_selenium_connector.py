import unittest
import os
import json
from connectors.selenium_connector import Selenium_Connector


class Test_System_Selenium_Connector(unittest.TestCase):


    def test_test_poc(self):
        sc = Selenium_Connector()

        self.assertEqual("Welcome to Python.org",sc.test_poc())

if __name__ == '__main__':
    unittest.main()
