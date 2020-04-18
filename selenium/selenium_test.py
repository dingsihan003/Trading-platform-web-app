from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import unittest, time
from selenium.webdriver.common.keys import Keys

class WebFunctions(unittest.TestCase):

    def setUp(self):
      while True:
        try:
          self.driver = webdriver.Remote(
     command_executor='http://selenium-chrome:4444/wd/hub',
     desired_capabilities=DesiredCapabilities.CHROME)
          break
        except:
          time.sleep(1)

    def test_home(self):
        driver = self.driver
        time.sleep(5)
        driver.get("http://web1:8000/home/")
        print(driver)
        print(driver.title)
        self.assertIn("Market", driver.title)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
