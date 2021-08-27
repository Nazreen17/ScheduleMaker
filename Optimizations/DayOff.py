from datetime import datetime

from Optimizations.DualShiftOptimizerStructure import DualShiftOptimizer


class DayOff(DualShiftOptimizer):
    def __init__(self, schedule_list=None, day_off=None):
        self.__day_off_int = self.__get_day_off_int(day_off) if day_off is not None else None
        super().__init__(schedule_list=schedule_list)

    @property
    def name(self):
        return "DayOff"

    @property
    def description(self):
        return "Get the schedules that have specific days with no classes (or closest possible to)"

    @property
    def result(self):
        result = "" if self.ties == [] else f"Total ties count: {len(self.ties)}"
        return result

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
                        raise ValueError(day_off)

        elif isinstance(day_off, int) and 0 <= day_off <= 6:
            # This is mainly for testing cases, since bot will use str inputs mainly
            return day_off

        else:
            raise TypeError(day_off)

    def compare_for_best(self, best, current):
        """
        compare_for_best() is called by the super class's __optimize() method.
        __optimize() compares the current and best case TermSchedule
        :param best:
        TermSchedule -> The best TermSchedule so far
        :param current:
        TermSchedule -> The current TermSchedule to compare to the best
        :return:
        TermSchedule -> Return the best case TermSchedule object
        """
        best_day = self.__get_day_off_list(best)
        current_day = self.__get_day_off_list(current)

        best_delta = self.__get_delta_time(best_day)
        current_delta = self.__get_delta_time(current_day)

        if current_delta == best_delta:
            self.ties_add_from_term_schedule(current)
            return best  # Default tie -> return previous best
        if best_delta < current_delta:  # return smallest delta
            return best
        else:
            self.ties = current  # Reset ties
            return current

    def __get_day_off_list(self, schedule_obj):
        day_off = []
        for class_obj in schedule_obj.classes:
            for meet_time_tuple in class_obj.class_time:
                if meet_time_tuple[0].weekday() == self.__day_off_int:
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
