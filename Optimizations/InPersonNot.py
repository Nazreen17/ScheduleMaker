from Optimizations.DualShiftOptimizerStructure import DualShiftOptimizer
from constants import CLASS_INSTRUCTION_IN_PERSON_KEYS


class Online(DualShiftOptimizer):
    def __init__(self, schedule_list=None):
        super().__init__(schedule_list=schedule_list)

    @property
    def name(self):
        return "Online"

    @property
    def description(self):
        return "Get the schedules that average end the most classes online"

    @property
    def result(self):
        result = "" if self.ties == [] else f"Total ties count: {len(self.ties)}"
        return result

    @staticmethod
    def __count_in_person(schedule_obj):
        """
        used in optimize
        :param schedule_obj:
        :return:
        """
        in_class_count = 0

        for class_obj in schedule_obj.classes:
            for key in CLASS_INSTRUCTION_IN_PERSON_KEYS:
                if class_obj.instruction is not None and key.lower() in class_obj.instruction.lower():
                    in_class_count += 1

        return in_class_count

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
        best_in_person_count = self.__count_in_person(best)
        current_in_person_count = self.__count_in_person(current)
        # LOWER IS BETTER

        if best_in_person_count == current_in_person_count:
            self.ties_add_from_term_schedule(current)
            return best  # Default tie -> return previous best
        elif best_in_person_count < current_in_person_count:
            return best
        else:  # else current_in_person_count < best_in_person_count
            self.ties = current  # Reset ties
            return current
