from Optimizations.DualShiftOptimizerStructure import DualShiftOptimizer


class Balanced(DualShiftOptimizer):
    def __init__(self, schedule_list=None):
        self.__target_timestamp_delta_average = None
        super().__init__(schedule_list=schedule_list)

    @property
    def name(self):
        return "Balanced"

    @property
    def description(self):
        return "Most balanced amount of time in class a day"

    @property
    def result(self):
        # Result string text
        result = "" if self.ties == [] else f"Total ties count: {len(self.ties)}"
        return result

    def __init_target_delta_average(self, initial_term_schedule_object):
        if self.__target_timestamp_delta_average is None:
            week_list = self.__timestamp_week_list_sum(initial_term_schedule_object)
            self.__target_timestamp_delta_average = sum(week_list) / len(week_list)  # Calculate mean as mean target
        else:
            raise RuntimeError("__target_delta_average has already been initialized")

    @staticmethod
    def __timestamp_week_list_sum(term_schedule_obj):
        """
        used in optimize
        :param term_schedule_obj:
        :return:
        list -> of 7 floats representing the sum timestamp of each day [Mon, Tue, Wed, Thu, Fri, Sat, Sun]
        """
        week_list = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        # Mon, Tue, Wed, Thu, Fri, Sat, Sun

        for class_obj in term_schedule_obj.classes:
            for class_time_tuple in class_obj.class_time:
                start_time = class_time_tuple[0]
                end_time = class_time_tuple[1]

                week_list[start_time.weekday()] += (end_time.timestamp() - start_time.timestamp())
                # time difference as a timestamp = end_time.timestamp() - start_time.timestamp()

        return week_list

    def __target_deviation(self, term_schedule_object):
        # Higher deviation_score is a higher deviation to the target (Better)

        week_list = self.__timestamp_week_list_sum(term_schedule_object)

        for day_i in range(len(week_list)):
            week_list[day_i] = abs(self.__target_timestamp_delta_average - week_list[day_i])  # Higher value = Greater
            # deviation

        return sum(week_list)

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
        if self.__target_timestamp_delta_average is None:
            self.__init_target_delta_average(best)

        best_case_target_deviation = self.__target_deviation(best)
        current_case_target_deviation = self.__target_deviation(current)
        # LESSER IS BETTER

        if best_case_target_deviation == current_case_target_deviation:  # Tie of scores
            self.ties_add_from_term_schedule(current)  # Add the current TermSchedule as a tied case
            return best  # Default tie -> return previous best

        elif best_case_target_deviation < current_case_target_deviation:  # Best case has a better score
            return best

        else:  # Current case has a better score
            self.ties = current  # Reset ties
            return current
