# Dev set program limits
MAX_OPTIMIZATIONS_PER_REQUEST = 5
MAX_COURSE_UPDATE_REQUESTS = 25

# Max schedule generation option combination limit
MAX_COURSE_COMBOS = 5000000

# Max schedule computation option amount per process
SINGLE_PROCESS_COMBOS = 500000

# Result generation filenames
CACHE_FILE_PATH = "Cache/"
SCHEDULE_PNG_FILENAME = "schedule.png"
RESULT_TXT_FILENAME = "result.txt"
CALENDAR_ICS_FILENAME = "calendar.ics"

# Used in internal computation for determining if an AClass object is in person (Compares to AClass.instruction str)
CLASS_INSTRUCTION_IN_PERSON_KEYS = ["In-class"]

# RGB Colour codes used for Pillow PNG schedule generation
RGB_ONLINE_BLUE = (157, 162, 233)
RGB_IN_PERSON_PEACH = (255, 223, 182)

# Public User Documentation - Google Doc
PUBLIC_USER_DOCUMENTATION_LINK = "https://tinyurl.com/4nrjc9hb"

# Github Link
GITHUB_REPO = "https://github.com/danielljeon/ScheduleMaker"

# Dev Server Invite Link
DEV_DISCORD_SERVER_LINK = "https://discord.gg/rg2gPxrgbg"
