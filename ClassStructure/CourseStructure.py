from datetime import datetime
import json


class ACourse:
    def __init__(self, fac, uid):
        self._fac = fac.upper()
        self._uid = uid.upper()

    @property
    def fac(self):
        return self._fac

    @fac.setter
    def fac(self, fac):
        if isinstance(fac, str):
            self._fac = fac.upper()
        else:
            raise TypeError

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, uid):
        if isinstance(uid, str):
            self._uid = uid.upper()
        else:
            raise TypeError

    def is_format_valid(self):
        """
        check if Course data is valid
        :return: bool
        """
        # shortest fac is "PHY", uid is always len 5 (1010U. 1850U, etc)
        if len(self._fac) >= 3 or len(self._uid) >= 5:
            return True
        else:
            return False

    def __str__(self):
        return str(self._fac) + str(self._uid)


class AClass(ACourse):
    def __init__(self, fac, uid):
        # crn=int, class_type=str, title=str, section=int, class_time=list, links=list, seats=int, capacity=int,
        # instruction=str, campus=str, building=str, room=str
        self._crn = None
        self._class_type = None
        self._title = None
        self._section = None
        self._class_time = None
        self._links = None
        self._seats = None
        self._capacity = None
        self._instruction = None
        self._campus = None
        self._building = None
        self._room = None
        super().__init__(fac, uid)

    def get_course(self):
        return ACourse(fac=self._fac, uid=self.uid)

    @property
    def crn(self):
        return self._crn

    @crn.setter
    def crn(self, crn):
        if isinstance(crn, str) or isinstance(crn, int):
            self._crn = int(crn)
        else:
            raise TypeError

    @property
    def class_type(self):
        return self._class_type

    @class_type.setter
    def class_type(self, class_type):
        if class_type.lower() not in ("lecture", "tutorial", "laboratory"):
            raise ValueError
        self._class_type = class_type

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if not isinstance(title, str):
            raise TypeError
        self._title = title

    @property
    def section(self):
        return self._section

    @section.setter
    def section(self, section):
        if isinstance(section, str) or isinstance(section, int):
            self._section = int(section)
        else:
            raise TypeError

    @property
    def class_time(self):
        return self._class_time

    @class_time.setter
    def class_time(self, class_time):
        if not isinstance(class_time, list) and class_time is not None:
            raise TypeError
        if isinstance(class_time, list):
            for inner_tuple in class_time:
                if not isinstance(inner_tuple, tuple):
                    raise TypeError
                if len(inner_tuple) != 2:
                    raise ValueError("Expected tuple len = 2; (start_datetime, end_datetime)")
                if not inner_tuple[1] > inner_tuple[0]:
                    raise ValueError("End time should be later than the Start time")
                for inner_datetime in inner_tuple:
                    if not isinstance(inner_datetime, datetime):
                        raise TypeError
        self._class_time = class_time

    @property
    def links(self):
        return self._links

    @links.setter
    def links(self, links):
        """
        links is a 2d list, each sublist holds a possible option
        :param links:
        :return:
        """
        if not isinstance(links, list):
            raise TypeError
        for i in range(len(links)):
            if not isinstance(links[i], list):
                raise TypeError
        self._links = links

    @property
    def seats(self):
        return self._seats

    @seats.setter
    def seats(self, seats):
        if isinstance(seats, str) or isinstance(seats, int):
            self._seats = int(seats)
        else:
            raise TypeError

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, capacity):
        if isinstance(capacity, str) or isinstance(capacity, int):
            self._seats = int(capacity)
        else:
            raise TypeError

    @property
    def instruction(self):
        return self._instruction

    @instruction.setter
    def instruction(self, instruction):
        self._instruction = instruction

    @property
    def campus(self):
        return self._campus

    @campus.setter
    def campus(self, campus):
        self._campus = campus

    @property
    def building(self):
        return self._building

    @building.setter
    def building(self, building):
        self._building = building

    @property
    def room(self):
        return self._room

    @room.setter
    def room(self, room):
        self._room = room

    def get_raw_str(self):
        links_str = ""
        if self._links is not None:
            for links_index in range(len(self._links)):
                links_str += str(self._links[links_index])

        class_time_str = ""
        if self._class_time is not None:
            for inner_tuple in self._class_time:
                start_time = inner_tuple[0]
                end_time = inner_tuple[1]
                class_time_str += "@" + str(start_time) + "~" + str(end_time)
                if self._class_time.index(inner_tuple) != len(self._class_time) - 1:
                    class_time_str += ", "

        return ("Course=" + str(self._fac) + " " + str(self._uid) + "\n" +
                "CRN=" + str(self._crn) + "\n" +
                "Title=" + str(self._title) + "\n" +
                "Type=" + str(self._class_type) + "\n" +
                "Section=" + str(self._section) + "\n" +
                "Time=" + class_time_str + "\n" +
                "Links=" + links_str + "\n" +
                "Seats=" + str(self._seats) + "\n" +
                "Instruction=" + str(self._instruction) + "\n" +
                "Campus=" + str(self._campus) + "\n" +
                "Building=" + str(self._building) + "\n" +
                "Room=" + str(self._room) + "\n" +
                "\n")

    def __str__(self):
        return self.get_raw_str()
