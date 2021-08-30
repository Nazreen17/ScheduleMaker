from datetime import datetime

# General Program Status Constants
# TODO ADJUST WITH NEW SEMESTER
CURRENT_TERM = "Fall 2021"

# Dev set program limits
# TODO DEV ADJUST
MAX_OPTIMIZATIONS_PER_REQUEST = 5
MAX_COURSE_UPDATE_REQUESTS = 25

MAX_COURSE_COMBOS = 5000000
SINGLE_PROCESS_COMBOS = 500000

# Result generation filenames
CACHE_FILE_PATH = "Cache/"
SCHEDULE_PNG_FILENAME = "schedule.png"
RESULT_TXT_FILENAME = "result.txt"
CALENDAR_CVS_FILENAME = "calendar.cvs"

# Semester Start End as datetime objects (CVSManipulation.py)
# TODO ADJUST WITH NEW SEMESTER
SEMESTER_START = datetime(2021, 9, 7, 0, 0)
SEMESTER_END = datetime(2021, 12, 6, 23, 59)
__READING_WEEK = (datetime(2021, 10, 11, 0, 0), datetime(2021, 10, 15, 23, 59))  # Thanksgiving Fall 2021 Reading Week
SEMESTER_EXCLUSION_TIMES = [__READING_WEEK]  # excluded meet time tuples, such as reading week

# Used in internal computation for determining if an AClass object is in person (Compares to AClass.instruction str)
# TODO DEV ADJUST
CLASS_INSTRUCTION_IN_PERSON_KEYS = ["In-class"]

# RGB Colour codes used for Pillow PNG schedule generation
RGB_ONLINE_BLUE = (157, 162, 233)
RGB_IN_PERSON_PEACH = (255, 223, 182)

# Public User Documentation - Google Doc
PUBLIC_USER_DOCUMENTATION_LINK = "https://docs.google.com/document/d/1zgVHCSHJoIqeGINdOmOBZsoW-tphYWR38JG_btiSBpA"
