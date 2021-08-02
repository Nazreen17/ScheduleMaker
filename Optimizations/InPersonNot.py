from Optimizations.Optimize import DualShiftOptimizerStructure


class Online(DualShiftOptimizerStructure):
    def __init__(self, schedule_list=None):
        self._name = "Online"
        self._description = "Get the schedules that average end the most classes online"
        self._max_schedules = schedule_list
        self._result = f"Total ties count: {len(super().ties)}"
        """
        WARNING! ATTRIBUTES RUN IN ORDER ^^^
        PUT RESULT AFTER optimal, UPDATE TIES AFTER optimize() TO MATCH _ties ATTRIBUTE
        (Or stop being lazy and make updater method)
        """
        super().__init__(name=self._name, description=self._description, max_schedule_list=self._max_schedules,
                         result=self._result)

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

    def compare_for_best(self, best, current):
        """
        Lower in_person_count is better
        :param best:
        :param current:
        :return:
        Return the TermSchedule object with the lowest in person count, in the case of a tie maintain the current best
        """
        best_in_person_count = self.__count_in_person(best)
        current_in_person_count = self.__count_in_person(current)

        if best_in_person_count == current_in_person_count:
            super().ties_append_via_term_schedule(current)
            return best  # Default tie -> return previous best
        elif best_in_person_count < current_in_person_count:
            return best
        else:  # else current_in_person_count < best_in_person_count
            super().ties = current  # Reset ties
            return current
