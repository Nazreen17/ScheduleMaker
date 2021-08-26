from Optimizations.DualShiftOptimizerStructure import DualShiftOptimizer


class OpenSeats(DualShiftOptimizer):
    def __init__(self, schedule_list=None):
        super().__init__(schedule_list=schedule_list)

    @property
    def name(self):
        return "OpenSeats"

    @property
    def description(self):
        return "Maximize open seat classes"

    @property
    def result(self):
        result = "" if self.ties == [] else f"Total ties count: {len(self.ties)}"
        return result

    @staticmethod
    def __open_seat_count(schedule_obj):
        """
        used in optimize
        :param schedule_obj:
        :return:
        """
        open_seats = 0

        for class_obj in schedule_obj.classes:
            if class_obj.seats > 0:
                open_seats += 1

        return open_seats

    def compare_for_best(self, best, current):
        """
        Higher in_person_count is better
        :param best:
        :param current:
        :return:
        Return the TermSchedule object with the most open seats
        """
        best_in_person_count = self.__open_seat_count(best)
        current_in_person_count = self.__open_seat_count(current)

        if best_in_person_count == current_in_person_count:
            self.ties_add_from_term_schedule(current)
            return best  # Default tie -> return previous best
        elif best_in_person_count > current_in_person_count:
            return best
        else:  # else current_in_person_count > best_in_person_count
            self.ties = current  # Reset ties
            return current
