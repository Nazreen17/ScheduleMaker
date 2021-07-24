#!/usr/bin/env python

class FlipClock:
    # The FlipClock represents the index of each option (kinda confusing here is example):
    # [0, 0, 1, 3] -> In this example, there are 4 clock digits, each digit represents a course and further the index
    # of the course option. So we could say that course 3 (index 3 of clock) is on option index 1.
    # All clocks start at initial values of all 0. [0, 0, 0, etc]
    def __init__(self, list_3d):
        self._clock = []
        self._limits = []
        self._shift_max = 0
        for course_index in range(len(list_3d)):
            self._clock.append(0)  # Clock starts at all zeros [0, 0, 0, etc]
            self._limits.append(len(list_3d[course_index]))
            # The clock assumes that all options have equal num of classes, thus take length of option 1 (index 0)
            # For example, we assume that each lecture has 2 linked classes (say 1 lab, 1 tutorial) per option,
            # so we can just take the length of option 1 (index 0) to get the max number of classes per option

    @property
    def clock(self):
        return self._clock

    @property
    def limits(self):
        return self._limits

    @property
    def shift_max(self):
        shift_max = 1
        for limit in self._limits:
            shift_max *= limit
        return shift_max

    def __getitem__(self, index):
        return self._clock[index]

    def shift(self):
        self._clock[-1] += 1
        for last_index in range(len(self._clock) - 1, -1, -1):  # if len(self._clock) = 5, -> 4, 3, 2, 1, 0
            if self._clock[last_index] == self._limits[last_index]:
                self._clock[last_index] = 0
                self._clock[last_index - 1] += 1

    def __check_limit(self):
        check_limit = []
        for i in range(len(self._limits)):
            check_limit.append(self._limits[i] - 1)
        return check_limit

    def __str__(self):
        return str(self._clock)


"""
TEST CODE
"""
"""
test = FlipClock([[1, 2, 3, 4, 5], [1, 2, 3], [1, 2, 3, 4]])
print("shift_max:", test.shift_max)

print(test)
for i in range(test.shift_max):  # 60 = 5 * 3 * 4, - 1 cause [0, 0, 0] is the initial clock combination done by default
    test.shift()
    print(test)
print("limits", test.limits)
"""
