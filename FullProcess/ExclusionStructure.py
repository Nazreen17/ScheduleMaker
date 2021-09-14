"""
Exclusion/Additional events universal to all student schedules
"""

from abc import ABC, abstractmethod


class Exclusion(ABC):
    def __init__(self, name, description, exclusion_time):
        self._name = name
        self._description = description
        self._exclusion_time = exclusion_time

    @abstractmethod
    def get_name(self):
        return self._name

    @abstractmethod
    def get_description(self):
        return self._description

    @abstractmethod
    def get_exclusion_times(self):
        return self._exclusion_time
