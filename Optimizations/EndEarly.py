#!/usr/bin/env python

from datetime import datetime

from Optimizations.Optimize import DualShiftOptimizerStructure
from ClassStructure.TermScheduleStructure import TermSchedule


class EndEarly(DualShiftOptimizerStructure):
    def __init__(self, schedule_list):
        self._name = "Early End"
        self._description = "Get the schedules that average end the earliest end times each class day"
        self._max_schedules = schedule_list
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

    @staticmethod
    def __generate_week_list(schedule_obj):
        """
        used in optimize
        :param schedule_obj:
        :return:
        """
        # generate a week list (default below vvv)
        week = [None, None, None, None, None, None, None]

        for class_obj in schedule_obj.classes:
            for inner_tuple in class_obj.class_time:
                if not isinstance(week[inner_tuple[1].weekday()], datetime) or \
                        week[inner_tuple[1].weekday()] < inner_tuple[1]:  # more recent in time
                    week[inner_tuple[1].weekday()] = inner_tuple[1]
        return week  # week list will have the latest class end times

    def __compare_for_best(self, best, current):
        """
        used in optimize
        :param best:
        :param current:
        :return:
        """
        best_week = self.__generate_week_list(best)
        current_week = self.__generate_week_list(current)

        # combining time deltas
        best_delta = datetime(1, 1, 1, 0, 0)
        current_delta = datetime(1, 1, 1, 0, 0)
        for day_i in range(7):
            if best_week[day_i] is not None:
                best_delta += best_week[day_i] - datetime(best_week[day_i].year, best_week[day_i].month,
                                                          best_week[day_i].day, 0, 0)
            if current_week[day_i] is not None:
                current_delta += current_week[day_i] - datetime(current_week[day_i].year, current_week[day_i].month,
                                                                current_week[day_i].day, 0, 0)
        if current_delta == best_delta:
            self._ties += 1
        if current_delta > best_delta:  # the greater the delta, the later classes end, return smallest delta
            return best
        else:
            self._ties = 0
            return current
