from datetime import datetime

from Optimizations.Optimize import DualShiftOptimizerStructure
from COREClassStructure.TermScheduleStructure import TermSchedule


class OffDay(DualShiftOptimizerStructure):
    def __init__(self, schedule_list=None, day_off=None):
        self._name = "DaysOff"
        self._description = "Get the schedules that have specific days with no classes (or closest possible to)"
        self._max_schedules = schedule_list
        self._day_off_int = self.__get_day_off_int(day_off) if day_off is not None else None
        self._ties = 0
        self._optimal = self.optimize()
        self._result = "Total ties: " + str(self._ties)
        """
        WARNING! ATTRIBUTES RUN IN ORDER ^^^
        PUT RESULT AFTER optimal, UPDATE TIES AFTER optimize() TO MATCH _ties ATTRIBUTE
        (Or stop being lazy and make updater method)
        """
        super().__init__(name=self._name, description=self._description, max_schedule_list=self._max_schedules,
                         result=self._result, optimal=self._optimal)

    @staticmethod
    def __get_day_off_int(day_off):
        if isinstance(day_off, str):
            day_off = day_off.lower().replace(" ", "")
            weekdays = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

            for weekday_partial in weekdays:
                if weekday_partial in day_off:  # Search the input str to see if the partial weekday name is within
                    return weekdays.index(weekday_partial)
                elif len(day_off) == 1 and day_off.isdigit():  # if the day int was passed as an int formatted in str
                    if 0 <= int(day_off) <= 6:
                        return int(day_off)
                    else:
                        raise ValueError
                else:
                    raise ValueError

        elif isinstance(day_off, int) and 0 <= day_off <= 6:
            # This is mainly for testing cases, since bot will use str inputs mainly
            return day_off

        else:
            raise ValueError

    def optimize(self):
        best = TermSchedule(self._max_schedules[0])  # initialized first element as the best case
        for crn_list_i in range(1, len(self._max_schedules)):  # cycle all in schedule list
            current = TermSchedule(self._max_schedules[crn_list_i])
            best = self.__compare_for_best(best, current)
        return best

    def __compare_for_best(self, best, current):
        """
        used in optimize
        :param best:
        :param current:
        :return:
        """
        best_day = self.__get_day_off_list(best)
        current_day = self.__get_day_off_list(current)

        best_delta = self.__get_delta_time(best_day)
        current_delta = self.__get_delta_time(current_day)

        if current_delta == best_delta:
            self._ties += 1
        if best_delta <= current_delta:  # return smallest delta
            return best
        else:
            self._ties = 0
            return current

    def __get_day_off_list(self, schedule_obj):
        day_off = []
        for class_obj in schedule_obj.classes:
            for meet_time_tuple in class_obj.class_time:
                if meet_time_tuple[0].weekday() == self._day_off_int:
                    day_off.append(meet_time_tuple)
        return day_off  # day off will have the meet time inner tuples

    @staticmethod
    def __get_delta_time(day):
        delta = datetime(1, 1, 1, 0, 0)  # deltas represent total class time on the int_day_off
        for element in day:
            start = datetime(1, 1, 1, element[0].hour, element[0].second)
            end = datetime(1, 1, 1, element[1].hour, element[1].second)
            delta += end - start
        return delta.time()
