from Optimizations.Optimize import DualShiftOptimizerStructure
from ClassStructure.SingleScheduleStructure import TermSchedule

from datetime import datetime


class OffDay(DualShiftOptimizerStructure):
    def __init__(self, schedule_list, day_off):
        self._name = "Days Off"
        self._description = "Get the schedules that have specific days with no classes (or closest possible to)"
        self._max_schedules = schedule_list
        if isinstance(day_off, str):
            weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
            if day_off.lower() in weekdays:
                self._day_off = weekdays.index(day_off.lower())
            elif len(day_off) == 1:  # if the day int was passed as an int accidentally
                try:
                    day_off = int(day_off)
                    if 0 <= day_off <= 6:
                        self._day_off = day_off
                except:
                    raise ValueError
            else:
                raise ValueError
        elif isinstance(day_off, int) and 0 <= day_off <= 6:
            self._day_off = day_off
        else:
            raise ValueError
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
                if meet_time_tuple[0].weekday() == self._day_off:
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
