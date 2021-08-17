# General Program Status Constants
CURRENT_TERM = "Fall 2021"

# Dev set program limits
MAX_OPTIMIZATIONS_PER_REQUEST = 3
MAX_COURSE_UPDATE_REQUESTS = 25

MAX_COURSE_COMBOS = 5000000
SINGLE_PROCESS_COMBOS = 500000

# Result generation filenames
CACHE_FILE_PATH = "Cache/"
SCHEDULE_PNG_FILENAME = "schedule.png"
RESULT_TXT_FILENAME = "result.txt"

# Used in internal computation for determining if an AClass object is in person (Compares to AClass.instruction str)
CLASS_INSTRUCTION_IN_PERSON_KEYS = ["In-class"]

# RGB Colour codes used for Pillow PNG schedule generation
RGB_ONLINE_BLUE = (157, 162, 233)
RGB_IN_PERSON_PEACH = (255, 223, 182)

# Public User Documentation - Google Doc
PUBLIC_USER_DOCUMENTATION_LINK = "https://docs.google.com/document/d/1zgVHCSHJoIqeGINdOmOBZsoW-tphYWR38JG_btiSBpA"
