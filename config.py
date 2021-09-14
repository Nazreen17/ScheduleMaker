from datetime import datetime
from FullProcess.ExclusionStructure import Exclusion

# General Program Status Constants
CURRENT_TERM = "Fall 2021"

# Semester Start End as datetime objects (CSVManipulation.py)
SEMESTER_START = datetime(2021, 9, 7, 0, 0)
SEMESTER_END = datetime(2021, 12, 6, 23, 59)

# Thanksgiving Fall 2021 Reading Week
__reading_week = Exclusion("Reading Week", "No class", [(datetime(2021, 10, 11, 0, 0), datetime(2021, 10, 15, 23, 59))])
# Fall 2021 Exam Period
__exams = Exclusion("Exam Period", "Exams", [(datetime(2021, 12, 8, 0, 0), datetime(2021, 12, 19, 23, 59))])

# ICS file enabled exclusion/additional events
ENABLED_EXCLUSIONS_LIST = [__reading_week, __exams]
