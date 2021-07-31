from abc import ABC, abstractmethod


class DualShiftOptimizerStructure(ABC):
    def __init__(self, name, description, max_schedule_list, result, optimal):
        self._name = name
        self._description = description
        self._max_schedules = max_schedule_list
        self._optimal = optimal
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
    def optimal(self):
        if self._optimal is None:
            try:
                self._optimal = self.optimize()
            except:
                self._optimal = None
        return self._optimal

    @property
    def result(self):
        return self._result

    @abstractmethod
    def optimize(self):
        pass
