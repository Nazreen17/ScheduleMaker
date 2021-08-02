from datetime import datetime

from Optimizations.Optimize import DualShiftOptimizerStructure
from COREClassStructure.TermScheduleStructure import TermSchedule


class InPerson(DualShiftOptimizerStructure):
    def __init__(self, schedule_list=None):
        self._name = "InPerson"
        self._description = "Get the schedules that average end the most classes in person"
        self._max_schedules = schedule_list
        self._ties = 0
        self._optimal = self.optimize() if schedule_list is not None else None
        self._result = "Total ties: " + str(self._ties)
        """
        WARNING! ATTRIBUTES RUN IN ORDER ^^^
        PUT RESULT AFTER optimal, UPDATE TIES AFTER optimize() TO MATCH _ties ATTRIBUTE
        (Or stop being lazy and make updater method)
        """
        super().__init__(name=self._name, description=self._description, max_schedule_list=self._max_schedules,
                         result=self._result, optimal=self._optimal)

    def optimize(self):
        best = TermSchedule(self._max_schedules[0])  # initialized first element as the best case
        for crn_list_i in range(1, len(self._max_schedules)):  # cycle all in schedule list
            current = TermSchedule(self._max_schedules[crn_list_i])
            best = self.__compare_for_best(best, current)
        return best

    @staticmethod
    def __count_in_person(schedule_obj):
        """
        used in optimize
        :param schedule_obj:
        :return:
        """
        instruction_type_in_person_keys = ["In-class"]
        in_class_count = 0

        for class_obj in schedule_obj.classes:
            for key in instruction_type_in_person_keys:
                if class_obj.instruction is not None and key in class_obj.instruction:
                    in_class_count += 1

        return in_class_count

    def __compare_for_best(self, best, current):
        """
        Higher in_person_count is better
        :param best:
        :param current:
        :return:
        Return the TermSchedule object with the highest in person count, in the case of a tie maintain the current best
        """
        best_in_person_count = self.__count_in_person(best)
        current_in_person_count = self.__count_in_person(current)

        if best_in_person_count == current_in_person_count:
            self._ties += 1
            return best  # Default tie -> return previous best
        elif best_in_person_count > current_in_person_count:
            return best
        else:  # else current_in_person_count > best_in_person_count
            self._ties = 0  # Reset ties
            return current
