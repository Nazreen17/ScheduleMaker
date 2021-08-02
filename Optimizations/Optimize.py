from abc import ABC, abstractmethod

from COREClassStructure.TermScheduleStructure import TermSchedule


class DualShiftOptimizerStructure(ABC):
    def __init__(self, schedule_list):
        self._max_schedules = schedule_list
        self._ties = []  # _ties attribute init must be called before _optimial init because _ties is required in
        # optimize(). The optimize() function is used in setting the _optimial value
        self._optimal = self.optimize() if self._max_schedules is not None else None

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def description(self):
        pass

    @property
    @abstractmethod
    def result(self):
        pass

    @property
    def optimal(self):  # Void property? Sets its own value when called
        if self._optimal is None:
            self._optimal = self.optimize()
        return self._optimal

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
