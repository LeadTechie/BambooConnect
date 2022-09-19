# library modulfrom selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.options import Options

#needs brew install --cask chromedriver

class Selenium_Connector:

    def __init__(self):
        self.project = ""

    def test_poc(self):
        #driver = webdriver.Chrome(ChromeDriverManager().install())
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = chrome_options)

        driver.get("https://www.python.org")
        #print

        return driver.title
