from datetime import datetime

from Optimizations.Optimize import DualShiftOptimizerStructure


class EarlyEnd(DualShiftOptimizerStructure):
    def __init__(self, schedule_list=None):
        super().__init__(schedule_list=schedule_list)

    @property
    def name(self):
        return "EarlyEnd"

    @property
    def description(self):
        return "Get the schedules that average end the earliest end times each class day"

    @property
    def result(self):
        result = "" if self.ties == [] else f"Total ties count: {len(self.ties)}"
        return result

    @staticmethod
    def __generate_week_list(term_schedule_obj):
        """
        used in optimize
        :param term_schedule_obj:
        :return:
        """
        # generate a week list (default below vvv)
        week = [None, None, None, None, None, None, None]

        for class_obj in term_schedule_obj.classes:
            for inner_tuple in class_obj.class_time:
                # TODO ERROR!!!
                #  class_obj is a list of class objects? I don't have time to fix... (too lazy)
                #  More details will be made on an issue on GitHub.
                if not isinstance(week[inner_tuple[1].weekday()], datetime) or \
                        week[inner_tuple[1].weekday()] < inner_tuple[1]:  # more recent in time
                    week[inner_tuple[1].weekday()] = inner_tuple[1]
        return week  # week list will have the latest class end times

    def compare_for_best(self, best, current):
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
            self.ties_append_via_term_schedule(current)
            return best  # Default tie -> return previous best
        if current_delta > best_delta:  # the greater the delta, the later classes end, return smallest delta
            return best
        else:
            self.ties = current  # Reset ties
            return current
