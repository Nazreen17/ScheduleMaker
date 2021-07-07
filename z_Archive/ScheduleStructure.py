from Structure.OptimizedOptionStructure import Option


class TermSchedule:
    """
    List of Options objects
    """

    def __init__(self, schedule):
        if not isinstance(schedule, list):
            raise TypeError
        for option_obj in schedule:
            if not isinstance(option_obj, Option):
                raise TypeError
        self._schedule = schedule

    @property
    def schedule(self):
        return self._schedule

    @schedule.setter
    def schedule(self, schedule):
        if not isinstance(schedule, list):
            raise TypeError
        for option_obj in schedule:
            if not isinstance(option_obj, Option):
                raise TypeError
        self._schedule = schedule

    def add(self, option_obj):
        if isinstance(option_obj, Option):
            self._schedule.append(option_obj)
        elif isinstance(option_obj, list):
            for possible in option_obj:
                if not isinstance(possible, Option):
                    raise TypeError
            self._schedule += option_obj

    def is_valid(self):
        """
        :return:
        True or False if a schedule is valid and does not have time conflicts
        """
        """
        test = main_schedules_list[0]
        print(type(test))
        print(type(test.schedule))
        print(type(test.schedule[0]))  # Option object at index 0
        print(type(test.schedule[0].busy))
        print(type(test.schedule[0].busy[0]))  # (each course option) Class ClassTime object
        print(type(test.schedule[0].busy[0].time_list))  # list of meet times
        print(type(test.schedule[0].busy[0].time_list[0]))  # (each class meet list) first meet time tuple
        print(type(test.schedule[0].busy[0].time_list[0][0]))  # start datetime
        print(type(test.schedule[0].busy[0].time_list[0][1]))  # end datetime
        """
        temp_hold = []
        for option_obj in self._schedule:
            for class_time_obj in option_obj.busy:
                for inner_tuple in class_time_obj.time_list:
                    temp_hold.append(inner_tuple)
        for inner_tuple_i in range(len(temp_hold)):
            start = temp_hold[inner_tuple_i][0]
            end = temp_hold[inner_tuple_i][1]
            for future_inner_tuple_i in range(inner_tuple_i + 1, len(temp_hold)):
                start2 = temp_hold[future_inner_tuple_i][0]
                end2 = temp_hold[future_inner_tuple_i][1]
                if start.weekday() == start2.weekday():
                    if start.time() <= start2.time() <= end.time() or start.time() <= end2.time() <= end.time() or \
                            start2.time() <= start.time() <= end2.time() or start2.time() <= end.time() <= end2.time():
                        return False
        return True

    def __len__(self):
        return len(self._schedule)

    def __str__(self):
        text_hold = "CRN="
        for option_obj in self._schedule:
            text_hold += str(option_obj.ids)
        return text_hold
