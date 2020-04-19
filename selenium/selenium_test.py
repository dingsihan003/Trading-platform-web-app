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
    
    def test_signup_login(self):
        driver = self.driver
        driver.get("http://web1:8000/signup/")
        username = driver.find_element_by_name("username")
        password = driver.find_element_by_name("password")
        email = driver.find_element_by_name("email")
        location = driver.find_element_by_name("location")
        submit = driver.find_element_by_name("submit")
        email.send_keys("selenium@test.com")
        username.send_keys("selenium")
        password.send_keys('test')
        submit.click()

        driver.get("http://web1:8000/login")
        driver.find_element_by_name("username").send_keys('selenium')
        driver.find_element_by_name("password").send_keys('test')
        driver.find_element_by_name('submit').click()
        self.assertIn("Market", driver.title)

        # driver.get('http://web1:8000/create_listing/')
        # button = driver.find_element_by_id('navbarDropdown')
        # button.click()
        # signout = driver.find_element_by_id('signout')
        # signout.click()
        # self.assertIn('Profile', driver.find_element_by_id('navbarDropdown').text)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
