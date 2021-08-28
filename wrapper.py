from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException



class SeleniumWrapper:

    def __init__(self, driver):
        self.driver = driver
    

    def wait_for_presence(self, locator, timeout=5):
        try:
            ele = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return ele
        except TimeoutException:
            return None
    

    def wait_for_presence_all(self, locator, timeout=5):
        try:
            elms = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
            return elms
        except TimeoutException:
            return None
    

    def wait_for_clickable(self, locator, timeout=5):
        try:
            ele = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            return ele
        except TimeoutException:
            return None
    

    def wait_for_title_contains(self, title_substring, timeout=5):
        try:
            ele = WebDriverWait(self.driver, timeout).until(
                EC.title_contains(title_substring)
            )
            return ele
        except TimeoutException:
            return None