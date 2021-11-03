from datetime import datetime
from FullProcess.ExclusionStructure import Exclusion

# Semester Start End as datetime objects
SEMESTER_START = datetime(2022, 1, 10, 0, 0)
SEMESTER_END = datetime(2022, 4, 9, 23, 59)

# Winter 2022 Reading Week
__reading_week = Exclusion(name="Reading Week", description="No class",
                           exclusion_time=[(datetime(2022, 2, 22, 0, 0), datetime(2022, 2, 27, 23, 59))])

# Winter 2022 Exam Period
__exams = Exclusion(name="Exam Period", description="Exams",
                    exclusion_time=[(datetime(2022, 4, 11, 0, 0), datetime(2022, 4, 24, 23, 59))])

# Winter 2022 Course change deadline
__course_change_deadline = Exclusion(name="Schedule change deadline",
                                     description="End of regular registration period; last day to add courses. Last "
                                                 "day to drop courses and receive a 100% refund of tuition and "
                                                 "ancillary fees, winter semester. Winter semester fees due.",
                                     exclusion_time=[(datetime(2022, 1, 21, 0, 0), datetime(2022, 1, 21, 23, 59))])

# Winter 2022 Course drop deadline
__course_drop_deadline = Exclusion(name="Last day to drop course",
                                   description="Last day to withdraw from winter semester courses without academic "
                                               "consequences (i.e., without receiving a grade). Courses dropped after "
                                               "this date will be recorded on the academic transcript with a grade of "
                                               "W to indicate withdrawal. Last day to drop courses and receive a 50% "
                                               "refund of tuition fees.",
                                   exclusion_time=[(datetime(2022, 2, 4, 0, 0), datetime(2022, 2, 4, 23, 59))])

# Family day
__family_day = Exclusion(name="Family Day",
                         description="Family Day, no scheduled academic activities.",
                         exclusion_time=[(datetime(2022, 2, 21, 0, 0), datetime(2022, 2, 21, 23, 59))])

ENABLED_EXCLUSIONS_LIST = [__reading_week, __exams, __course_change_deadline, __course_drop_deadline, __family_day]
# ICS file enabled exclusion/additional events
