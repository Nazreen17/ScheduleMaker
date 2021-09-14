"""
Exclusion/Additional events universal to all student schedules
"""

from abc import ABC


class Exclusion(ABC):
    def __init__(self, exclusion_time, name=None, description=None):
        self._name = name if name is not None else "None"
        self._description = description if description is not None else "None"
        self._exclusion_time = exclusion_time
        # exclusion time format example: [(datetime(2021, 12, 8, 0, 0), datetime(2021, 12, 19, 23, 59))]

    def get_name(self):
        return self._name

    def get_description(self):
        return self._description

    def get_exclusion_times(self):
        return self._exclusion_time
