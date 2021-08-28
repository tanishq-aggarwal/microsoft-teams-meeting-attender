from wrapper import SeleniumWrapper
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import re


class MeetingHandler:

    def __init__(self, driver):
        self.selenium = SeleniumWrapper(driver)
        self.current_meeting = {}
    

    def check_ongoing_meeting(self):
        if self.selenium.wait_for_presence(locator=(By.ID, "hangup-button"), timeout=5):
            return True
        return False
    

    def prepare_calendar(self):
        calendar_button = self.selenium.wait_for_clickable(
            locator=(By.CSS_SELECTOR, "[aria-label='Calendar Toolbar']"),
            timeout=5
        )
        if not calendar_button: raise Exception("[-] Unable to find Calendar button. Make sure the browser window is maximized and it is visible in the navigation bar.")
        calendar_button.click()

        view_list_button = self.selenium.wait_for_clickable(
            locator=(By.CSS_SELECTOR, "button[title='Switch your calendar view']"),
            timeout=5
        )
        if not view_list_button: raise Exception("[-] Unable to switch to day view.")
        view_list_button.click()
        
        time.sleep(1)

        day_view_button = self.selenium.wait_for_presence(
            locator=(By.CSS_SELECTOR, "button[aria-label='Day view']"),
            timeout=5
        )
        if not day_view_button: raise Exception("[-] Unable to switch to day view.")
        day_view_button.click()


    def get_next_meeting_element(self):
        # All meeting card elements contain "from <> to <>" in their title attributes
        available_meetings = self.selenium.wait_for_presence_all(
            locator=(By.CSS_SELECTOR, "[title*='from'"), timeout=5
        )
        if not available_meetings: raise Exception("[-] Could not find any meetings on today's calendar")
        
        for meeting in available_meetings:
            result = re.search(".*from (.*?) to (.*?)$", meeting.get_attribute("title"))
            meeting_start = datetime.strptime(result.group(1), "%I:%M %p").time()
            meeting_end = datetime.strptime(result.group(2), "%I:%M %p").time()
            current_time = datetime.now().time()
            if meeting_start <= current_time < meeting_end:
                return {
                    "ele": meeting,
                    "title": meeting.get_attribute("title"),
                    "starts_at": meeting_start,
                    "ends_at": meeting_end
                }
        return {}
    

    def attend_new_meeting(self):
        self.current_meeting.get("ele").click()
        
        # Click on "Join" button
        join_button = self.selenium.wait_for_presence(
            locator=(By.CSS_SELECTOR, "[data-tid='calv2-peek-join-button']"),
            timeout=5
        )
        if not join_button: raise Exception("[-] Could not find Join button after clicking meeting card. Make sure it is visible on the screen.")
        join_button.click()

        # Click on "Continue without audio or video" button if it appears
        print("[+] Checking for appearance of 'Continue without audio or video' button")
        continue_without_audio_button = self.selenium.wait_for_presence(
            locator=(By.CSS_SELECTOR, "[ng-click='getUserMedia.passWithoutMedia()']"),
            timeout=3
        )
        if continue_without_audio_button: continue_without_audio_button.click()

        # Turn off mic
        print("[+] Turning off mic (if not already off)")
        mic_off_button = self.selenium.wait_for_presence(
            locator=(By.CSS_SELECTOR, "toggle-button[title='Mute microphone']"),
            timeout=3
        )
        if mic_off_button: mic_off_button.click()

        # Turn off webcam
        print("[+] Turning off webcam (if not already off)")
        webcam_off_button = self.selenium.wait_for_presence(
            locator=(By.CSS_SELECTOR, "toggle-button[title='Turn camera off']"),
            timeout=3
        )
        if webcam_off_button: webcam_off_button.click()

        # Join meeting
        print("[+] Joining meeting")
        pre_join_button = self.selenium.wait_for_clickable(
            locator=(By.CSS_SELECTOR, "button[aria-label='Join the meeting']"),
            timeout=3
        )
        if not pre_join_button: raise Exception("[-] Could not find Join button. Make sure it is visibile on the screen.")
        pre_join_button.click()
    

    def end_meeting(self):
        hangup_button = self.selenium.wait_for_clickable(locator=(By.ID, "hangup-button"), timeout=5)
        if not hangup_button: raise Exception("[-] Could not find hangup button to exit meeting. Make sure it is visible on the screen, or exit the meeting manually.")
        hangup_button.click()
    

    def handle(self):
        if not self.check_ongoing_meeting():
            print("[+] Currently not in a meeting. Will proceed to join the next meeting on the calendar.")
            self.prepare_calendar()
            next_meeting = self.get_next_meeting_element()
            if next_meeting:
                print("[+] Found meeting: {}. Will proceed to attending meeting.".format(next_meeting.get("title")))
                self.current_meeting = next_meeting
                self.attend_new_meeting()
        else:
            current_time = datetime.now().time()
            if self.current_meeting and self.current_meeting["starts_at"] <= current_time < self.current_meeting["ends_at"]:
                print("[+] Currently attending: {}. Will check for a new meeting at {}".format(
                    self.current_meeting["title"],
                    self.current_meeting["ends_at"].strftime("%I:%M %p")
                ))
            else:
                print("[+] Exiting meeting: {}".format(self.current_meeting.get("title")))
                self.end_meeting()