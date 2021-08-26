from abc import ABC, abstractmethod

from COREClassStructure.TermScheduleStructure import TermSchedule


class DualShiftOptimizer(ABC):
    def __init__(self, schedule_list):
        self._max_schedules = schedule_list
        self._ties = []  # list -> List of TermSchedule objects tied for the best case of the requested Optimizer
        # _ties attribute init must be called before _optimal init because _ties is required in optimize().
        # The optimize() function is used in calculating and setting the _optimal value

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
        """
        void -> Calculate the ties attribute/property and set the self._ties attribute
        """
        if len(self._max_schedules) == 0:
            raise ValueError("len(max_schedules) = 0")

        best = TermSchedule(self._max_schedules[0])  # Initialized first element as the best case
        self._ties.append(best)  # Initialize best into the ties

        for crn_list_i in range(1, len(self._max_schedules)):  # cycle all in schedule list
            current = TermSchedule(self._max_schedules[crn_list_i])
            best = self.compare_for_best(best, current)

    @abstractmethod
    def compare_for_best(self, best, current):
        """
        Check __OptimizerExample() from OptimizerExample.py for an example
        Abstract method is pushed to a a subclass

        compare_for_best() is called by the super class's __optimize() method.
        __optimize() compares the current and best case TermSchedule
        :param best:
        TermSchedule -> The best TermSchedule so far
        :param current:
        TermSchedule -> The current TermSchedule to compare to the best
        :return:
        TermSchedule -> Return the best case TermSchedule object
        """
        pass

    @property
    def ties(self):
        """
        property getter
        :return:
        attribute -> self._ties
        """
        return self._ties

    def ties_add_from_term_schedule(self, term_schedule):
        """
        void -> Should/Is called during compare_for_best() to add a new TermSchedule in the case of a tie
        :param term_schedule:
        TermSchedule -> Object to add to the attribute list
        """
        if isinstance(term_schedule, TermSchedule):
            self._ties.append(term_schedule)
        else:
            raise TypeError(term_schedule)

    @ties.setter
    def ties(self, ties):
        """
        property setter (Setter mostly used for testing purposes)
        :param ties:
        TermSchedule, list, tuple -> Set as the new ties
        """
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
