from ClassStructure.CourseStructure import AClass


class TermSchedule:
    def __init__(self, classes=None):
        if isinstance(classes, list):
            for a_class in classes:
                if not isinstance(a_class, AClass):
                    raise TypeError
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

    def __len__(self):
        return len(self._classes)

    def __str__(self):
        text_hold = ""
        for class_obj in self._classes:
            text_hold += class_obj.get_raw_str()
        return text_hold
