import json
from datetime import datetime

from ClassStructure.CourseClassStructure import AClass


class MaxSchedule:
    def __init__(self, crn_list=None, class_times_list=None):
        if isinstance(crn_list, list):
            for crn in crn_list:
                if not isinstance(crn, str):
                    raise TypeError
            self._crn_list = crn_list
        elif crn_list is None:
            self._crn_list = []
        else:
            raise TypeError
        if isinstance(class_times_list, list):
            for inner_tuple in class_times_list:
                if not isinstance(inner_tuple, tuple):
                    raise TypeError
                for datetime_obj in inner_tuple:
                    if not isinstance(datetime_obj, datetime):
                        raise TypeError
                    self._class_times_list.append(datetime_obj)
        elif class_times_list is None:
            self._class_times_list = []
        else:
            raise TypeError

    @property
    def crn_list(self):
        return self._crn_list

    @crn_list.setter
    def crn_list(self, crn_list):
        if not isinstance(crn_list, list):
            raise TypeError
        for crn in crn_list:
            if not isinstance(crn, str):
                raise TypeError
        self._crn_list = crn_list

    @property
    def class_times_list(self):
        return self._class_times_list

    @class_times_list.setter
    def class_times_list(self, class_times_list):
        if not isinstance(class_times_list, list):
            raise TypeError
        for inner_tuple in class_times_list:
            if not isinstance(inner_tuple, tuple):
                raise TypeError
            for datetime_obj in inner_tuple:
                if not isinstance(datetime_obj, datetime):
                    raise TypeError
                self._class_times_list.append(datetime_obj)

    def add_from_class(self, classes):
        if isinstance(classes, AClass):
            self._crn_list.append(classes.crn)
            for inner_tuple in classes.class_time:
                for datetime_obj in inner_tuple:
                    if not isinstance(datetime_obj, datetime):
                        raise TypeError
                    self._class_times_list.append(datetime_obj)
        elif isinstance(classes, list):
            for a_class in classes:
                if isinstance(a_class, AClass):
                    self._crn_list.append(a_class.crn)
                    for inner_tuple in a_class.class_time:
                        for datetime_obj in inner_tuple:
                            if not isinstance(datetime_obj, datetime):
                                raise TypeError
                            self._class_times_list.append(datetime_obj)
                else:
                    raise TypeError
        else:
            raise TypeError

    def is_valid(self):
        """
        :return:
        True or False if a schedule is valid and does not have time conflicts
        """
        for datetime_obj_i in range(0, len(self._class_times_list) - 4, 2):
            start = self._class_times_list[datetime_obj_i]
            end = self._class_times_list[datetime_obj_i + 1]
            for datetime_obj2_i in range(datetime_obj_i + 2, len(self._class_times_list) - 2, 2):
                start2 = self._class_times_list[datetime_obj2_i]
                end2 = self._class_times_list[datetime_obj2_i + 1]
                if start.weekday() == start2.weekday():
                    if start.time() <= start2.time() <= end.time() or start.time() <= end2.time() <= end.time() or \
                            start2.time() <= start.time() <= end2.time() or start2.time() <= end.time() <= end2.time():
                        return False
        return True

    def __len__(self):
        return len(self._crn_list)

    def __str__(self):
        return str(self._crn_list)


class TermScheduleDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    @staticmethod
    def object_hook(dct):
        class_obj = AClass(dct["_fac"], dct["_uid"])
        class_obj.crn = dct["_crn"]

        class_time = []
        for inner_list in dct["_class_time"]:
            class_time.append((datetime.fromisoformat(inner_list[0]), datetime.fromisoformat(inner_list[1])))
        class_obj.class_time = class_time  # datetime.fromisoformat()

        class_obj.seats = dct["_seats"]
        return class_obj
