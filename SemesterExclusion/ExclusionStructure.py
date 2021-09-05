"""
Exclusion times universal in all schedules
"""

from abc import ABC, abstractmethod


class Exclusion(ABC):
    @staticmethod
    @abstractmethod
    def get_name():
        pass

    @staticmethod
    @abstractmethod
    def get_description():
        pass

    @staticmethod
    @abstractmethod
    def get_exclusion_times():
        pass
