from SemesterExclusion.ExclusionStructure import Exclusion
from datetime import datetime


class ReadingWeek(Exclusion):
    @staticmethod
    def get_name():
        return "Reading Week"

    @staticmethod
    def get_description():
        return "No class"

    @staticmethod
    def get_exclusion_times():
        return [(datetime(2021, 10, 11, 0, 0), datetime(2021, 10, 15, 23, 59))]  # Thanksgiving Fall 2021 Reading Week
