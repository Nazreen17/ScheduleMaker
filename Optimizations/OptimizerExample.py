from Optimizations.DualShiftOptimizerStructure import DualShiftOptimizer


class __OptimizerExample(DualShiftOptimizer):
    def __init__(self, schedule_list=None):
        super().__init__(schedule_list=schedule_list)

    @property
    def name(self):
        return "OptimizerExampleName"

    @property
    def description(self):
        return "Optimizer Description (What the optimizer does)"

    @property
    def result(self):
        # Result string text
        result = "" if self.ties == [] else f"Total ties count: {len(self.ties)}"
        return result

    @staticmethod
    def __calculate_score(term_schedule_obj):
        """
        used in optimize
        :param term_schedule_obj:
        TermSchedule -> Calculate score of this TermSchedule
        :return:
        """
        example_score = 0

        for class_obj in term_schedule_obj.classes:
            pass

        return example_score

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
        best_case_score = self.__calculate_score(best)
        current_case_score = self.__calculate_score(current)

        if best_case_score == current_case_score:  # Tie of scores
            self.ties_add_from_term_schedule(current)  # Add the current TermSchedule as a tied case
            return best  # Default tie -> return previous best

        elif best_case_score > current_case_score:  # Best case has a better score
            return best

        else:  # Current case has a better score
            self.ties = current  # Reset ties
            return current
