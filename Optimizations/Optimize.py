from abc import ABC, abstractmethod

from COREClassStructure.TermScheduleStructure import TermSchedule


class DualShiftOptimizerStructure(ABC):
    def __init__(self, name, description, max_schedule_list, result):
        self._name = name
        self._description = description
        self._max_schedules = max_schedule_list
        self._optimal = None
        self._ties = []
        self._result = result
        """
        WARNING! ATTRIBUTES RUN IN ORDER ^^^
        PUT RESULT AFTER optimal, UPDATE TIES AFTER optimize() TO MATCH _ties ATTRIBUTE
        (Or stop being lazy and make updater method)
        """

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def max_schedules(self):
        return self._max_schedules

    @max_schedules.setter
    def max_schedules(self, max_schedule_list):
        self._max_schedules = max_schedule_list

    @property
    def optimal(self):  # Void property? Sets its own value when called
        if self._optimal is None:
            try:
                self._optimal = self.optimize()
            except:
                self._optimal = None
        return self._optimal

    @property
    def result(self):
        return self._result

    def optimize(self):
        best = TermSchedule(self._max_schedules[0])  # Initialized first element as the best case
        self._ties.append(best.classes)  # Initialize best into the ties
        for crn_list_i in range(1, len(self._max_schedules)):  # cycle all in schedule list
            current = TermSchedule(self._max_schedules[crn_list_i])
            best = self.compare_for_best(best, current)
        return best

    @abstractmethod
    def compare_for_best(self, best, current):
        pass

    @property
    def ties(self):
        return self._ties

    def ties_append_via_term_schedule(self, term_schedule_object):
        self._ties.append(term_schedule_object.classes)

    @ties.setter
    def ties(self, ties):
        if isinstance(ties, TermSchedule):
            self._ties = ties.classes
        elif isinstance(ties, list):
            self._ties = ties
        elif isinstance(ties, tuple):
            self._ties = list(ties)
