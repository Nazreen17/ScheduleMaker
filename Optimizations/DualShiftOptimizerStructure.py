from abc import ABC, abstractmethod

from COREClassStructure.TermScheduleStructure import TermSchedule


class DualShiftOptimizer(ABC):
    def __init__(self, schedule_list):
        self._max_schedules = schedule_list
        self._ties = []
        # _ties attribute init must be called before _optimal init because _ties is required in optimize().
        # The optimize() function is used in setting the _optimal value
        if self._max_schedules is not None and self._ties == []:
            self.__optimize()

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

    def __optimize(self):
        best = TermSchedule(self._max_schedules[0])  # Initialized first element as the best case
        self._ties.append(best)  # Initialize best into the ties
        for crn_list_i in range(1, len(self._max_schedules)):  # cycle all in schedule list
            current = TermSchedule(self._max_schedules[crn_list_i])
            best = self.compare_for_best(best, current)

    @abstractmethod
    def compare_for_best(self, best, current):
        pass

    @property
    def ties(self):
        return self._ties

    def ties_add_from_term_schedule(self, term_schedule):
        if isinstance(term_schedule, TermSchedule):
            self._ties.append(term_schedule)
        else:
            raise TypeError(term_schedule)

    @ties.setter
    def ties(self, ties):
        if isinstance(ties, TermSchedule):
            self._ties = [ties]
        elif isinstance(ties, list):
            self._ties = ties
        elif isinstance(ties, tuple):
            self._ties = list(ties)

    def __str__(self):
        return (f"--- DualShiftOptimizer (SubClass) Object ---\n"
                f"name = {self.name}\n"
                f"description = {self.description}\n"
                f"result = {self.result}\n"
                f"ties = {self.ties}")
