class Option:
    def __init__(self, *args):
        self._ids = []
        self._busy = []  # list of ClassTime objects
        for class_object in args:
            self._ids.append(class_object.crn)
            self._busy.append(class_object.class_time)

    @property
    def ids(self):
        return self._ids

    @ids.setter
    def ids(self, ids):
        self._ids = ids

    def add_ids_from(self, class_object):
        self._ids.append(class_object.crn)

    @property
    def busy(self):
        return self._busy

    @busy.setter
    def busy(self, busy):
        self._busy = busy

    def add_busy_from(self, class_object):
        self._busy.append(class_object.class_time)

    def add(self, *args):
        for class_object in args:
            self.add_ids_from(class_object)
            self.add_busy_from(class_object)

    def __len__(self):
        return len(self._ids)

    def __str__(self):
        return "CRN=" + str(self.ids)
