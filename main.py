from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
from wrapper import SeleniumWrapper
from page_detect import PageDetector
from meeting_handler import MeetingHandler
from login_handler import LoginHandler



def load_config():
    config = json.load(open("config.json"))
    assert config.get("email"), "Oh no! You forgot to specify an e-mail in config.json"
    assert config.get("password"), "Oh no! You forgot to specify a password in config.json"
    return config



def init_browser(config):
    options = webdriver.ChromeOptions()
    if config.get("chrome_profile_path"):
        options.add_argument("user-data-dir=" + config.get("chrome_profile_path"))
    if config.get("mute_audio"):
        options.add_argument("--mute-audio")
    if config.get("headless"):
        options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    return driver



def main():
    config = load_config()

    driver = init_browser(config)
    driver.maximize_window()
    driver.get("https://teams.microsoft.com/")
    driver.implicitly_wait(10)  # Always give ~10 seconds for the DOM to finish processing

    # Instantiate classes 
    selenium = SeleniumWrapper(driver)
    page_detector = PageDetector(driver)
    meeting_handler = MeetingHandler(driver)
    login_handler = LoginHandler(driver, config)

    # Start main loop
    while True:
        try:
            current_page = page_detector.detect()
            if current_page == "main-app-page":
                print("[+] Detected main app page. Proceeding to meeting detection.")
                meeting_handler.handle()
            elif current_page == "promo-page":
                print("[+] Detected desktop app promo page. Clicking on continue button.")
                continue_button = selenium.wait_for_clickable(locator=(By.CLASS_NAME, "use-app-lnk"), timeout=5)
                if continue_button: continue_button.click()
            elif current_page == "sign-in-page":
                print("[+] Detected sign in page. Attempting to login.")
                login_handler.handle()
            else:
                print("[-] Detected an unknown page. Refreshing Microsoft Teams.")
                driver.get("https://teams.microsoft.com/")
            time.sleep(10)
        except Exception as e:
            print(e)
            time.sleep(10)



if __name__ == "__main__":
    main()