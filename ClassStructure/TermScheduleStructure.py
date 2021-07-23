#!/usr/bin/env python

import os

from ClassStructure.CourseClassStructure import AClass, extract_from_json_str


class TermSchedule:
    def __init__(self, classes=None):
        if isinstance(classes, list):
            for element_i in range(len(classes)):
                if not isinstance(classes[element_i], AClass):
                    temp = self.__extract_from_crn(classes[element_i])
                    if temp is not None:
                        classes[element_i] = temp
                    else:
                        raise ValueError("Class with crn=" + str(classes[element_i]) + " does not exist")
            self._classes = classes
        elif classes is None:
            self._classes = []
        else:
            raise TypeError

    @property
    def classes(self):
        return self._classes

    @classes.setter
    def classes(self, classes):
        if not isinstance(classes, list):
            raise TypeError
        for a_class in classes:
            if not isinstance(a_class, AClass):
                raise TypeError
        self._classes = classes

    def add_class(self, classes):
        if isinstance(classes, AClass):
            classes = AClass(fac=classes.fac, uid=classes.uid, class_time=classes.class_time, seats=classes.seats)
            self._classes.append(classes)
        elif isinstance(classes, list):
            for obj_i in range(len(classes)):
                if not isinstance(classes[obj_i], AClass):
                    raise TypeError
            self._classes += classes

    def is_valid(self):
        """
        :return:
        True or False if a schedule is valid and does not have time conflicts
        """
        temp_hold = []
        for class_obj in self._classes:
            for inner_tuple in class_obj.class_time:
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

    @staticmethod
    def __extract_from_crn(crn):
        path_to_json = "..//JSONCourses/"
        json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

        for json_file in json_files:
            temp = extract_from_json_str(json_file)
            for a_class in temp:
                if a_class.crn == crn:
                    return a_class
        return None

    def __len__(self):
        return len(self._classes)

    def __str__(self):
        text_hold = ""
        for class_obj in self._classes:
            text_hold += class_obj.get_raw_str()
        return text_hold
