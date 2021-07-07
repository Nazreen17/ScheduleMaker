"""
Constants Used in Program
"""

STOP_CODES = ["stop", "exit", "end", "done"]

# selenium and chromedriver stuff
CHROMEDRIVER_PATH = r"C:\Users\idani\Desktop\chromedriver.exe"
OTU_COURSE_WEBSITE = "https://ssp.mycampus.ca/StudentRegistrationSsb/ssb/term/termSelection?mode=search&mepCode=UOIT"

# driver search keys in x paths and text input boxes
TERM = "Fall 2021"
TERM_ID = "202109"

# datetime correction for printing
WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

# selenium and chromedriver time.sleep() wait times
SLEEP_GENERAL = 1  # search results, next page load times, etc
SLEEP_NEXT_CLASS = .2  # wait before reading next class in table
SLEEP_TEXT_INPUT = .7  # wait before typing in text into a text input box
SLEEP_DETAIL_POPUP_TAB = .5
SLEEP_DETAIL_POPUP_TAB_TEXT = .3
