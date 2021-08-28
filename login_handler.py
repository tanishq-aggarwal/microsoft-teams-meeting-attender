from wrapper import SeleniumWrapper
from selenium.webdriver.common.by import By
import time



class LoginHandler:

    def __init__(self, driver, config):
        self.selenium = SeleniumWrapper(driver)
        self.config = config
    

    def handle(self):
        print("[+] Checking for presence of 'Pick an account' screen")
        use_another_account_button = self.selenium.wait_for_presence(locator=(By.ID, "otherTile"), timeout=5)
        if use_another_account_button: use_another_account_button.click()

        email_input = self.selenium.wait_for_presence(locator=(By.NAME, "loginfmt"), timeout=5)
        if not email_input:
            print("[-] Could not detect e-mail input field. Script will pause for 60 seconds to enable you to login manually.")
            time.sleep(60)
            raise Exception("")
        email_input.send_keys(self.config.get("email"))

        time.sleep(2)

        next_button = self.selenium.wait_for_clickable(locator=(By.ID, "idSIButton9"), timeout=5)
        if next_button: next_button.click()

        time.sleep(2)

        password_input = self.selenium.wait_for_presence(locator=(By.NAME, "passwd"), timeout=5)
        if not password_input:
            print("[-] Could not detect password input field. Script will pause for 60 seconds to enable you to login manually.")
            time.sleep(60)
            raise Exception("")
        password_input.send_keys(self.config.get("password"))

        time.sleep(2)

        next_button = self.selenium.wait_for_clickable(locator=(By.ID, "idSIButton9"), timeout=5)
        if next_button: next_button.click()

        print("[+] Checking for appearance of additional verification screen")
        verify_screen = self.selenium.wait_for_presence(
            locator=(By.XPATH, "//*[text()='Verify your identity']"),
            timeout=5
        )
        if verify_screen:
            print("[-] Additional verification required. Script will pause for 60 seconds to enable you to login manually.")
            time.sleep(60)