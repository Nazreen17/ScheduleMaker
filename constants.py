# Dev set limiters
MAX_SCHEDULE_COMBINATIONS = 100000
MAX_OPTIMIZATIONS_PER_REQUEST = 3
MAX_COURSE_UPDATE_REQUESTS = 25

# Used in internal computation for determining if an AClass object is in person (Compares to AClass.instruction str)
CLASS_INSTRUCTION_IN_PERSON_KEYS = ["In-class"]

# RGB Colour codes used for Pillow PNG schedule generation
RGB_ONLINE_BLUE = (157, 162, 233)
RGB_IN_PERSON_PEACH = (255, 223, 182)
