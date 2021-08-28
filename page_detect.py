from wrapper import SeleniumWrapper
from selenium.webdriver.common.by import By



class PageDetector:

    def __init__(self, driver):
        self.selenium = SeleniumWrapper(driver)
    

    def detect(self):
        if self.selenium.wait_for_presence(locator=(By.ID, "teams-app-bar"), timeout=30):
            if self.selenium.wait_for_presence(locator=(By.ID, "download-desktop-page"), timeout=3):
                return "promo-page"
            return "main-app-page"
        elif self.selenium.wait_for_title_contains(title_substring="Sign in", timeout=30):
            return "sign-in-page"
        else:
            return "unknown"