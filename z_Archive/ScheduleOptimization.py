from DBv1Courses.ExtractionDBv1 import extract
from DBv1Schedules.DBv1ScheduleFileManip import schedules_read
from Structure.CourseStructure import ACourse

from datetime import datetime
import time


def optimize():
    file_name = input("Enter a schedule.txt file to use > ")
    exec_start = time.time()

    print("\t1) Extracting schedule data...")
    extracted_schedule = schedules_read(file_name)  # list of class_objects from DBv1Courses

    print("\t2) Creating course objects from schedule data (line 0)...")
    course_list = __schedule_txt_to_course_obj_list(extracted_schedule[0])

    print("\t3) Creating class objects from course objects...")
    extracted_classes = extract(course_list)

    print("\t4) Extracting CRN data from schedule data...")
    options = []
    for crn_option_index in range(1, len(extracted_schedule)):  # index 0 (line 1) is course data
        options.append(__extract_from_schedule_text(extracted_schedule[crn_option_index]))
    # options now = [[option1 int crn codes], [option2 int crn codes], [option3 int crn codes], etc]

    print("\t5) Matching class objects to schedule CRNs...")
    for option_i in range(len(options)):
        temp = []
        for str_crn in options[option_i]:
            for course_sublist in extracted_classes:
                for class_obj in course_sublist:
                    if class_obj.crn == str_crn:
                        temp.append(class_obj)
        options[option_i] = temp
    # options now = [[option1 Lecture/Secondary], [option2 Lecture/Secondary], [option3 Lecture/Secondary], etc]

    print("\t6) Running optimizations...")
    best_case_option = options[0]  # default best case to first option class sublist
    for option_i in range(1, len(options)):
        # TODO Weird bug here? Passing best_case_option into the __optimize functions causes a None type to be passed.
        #  But the __optimize functions work if you pass options[0] directly as the best case?

        # best_case_option = __optimize_end_early(options[option_i], best_case_option)
        best_case_option = __optimize_day_off(options[option_i], best_case_option, 3)

    print("\tOptimized schedules found in", str(round(time.time() - exec_start, 2)) + "sec")

    for thing in best_case_option:
        print(__print_class_info(thing))


def __extract_from_schedule_text(crn_text):
    """
    :param crn_text:
    :return:
    returns a list of crn in datatype int
    """
    crn_text = crn_text[crn_text.index("=") + 1:]
    crn_text = crn_text.replace(" ", "").replace("][", ",").replace("[", "").replace("]", "").replace("\n", "")

    crn_int_list = []
    while True:
        try:
            crn_data = crn_text[:crn_text.index(",")]
            crn_text = crn_text[crn_text.index(",") + 1:]
            crn_int_list.append(int(crn_data))
        except ValueError:  # end of all options (no longer can find index of "[")
            crn_data = crn_text
            crn_int_list.append(int(crn_data))
            return crn_int_list


def __schedule_txt_to_course_obj_list(course_read_line):
    """
    original code stolen from Menu.py LOL -> IM A MONKEY, DO NOT COPY PASTE CODE
    :return:
    return the a list of Course objects
    """
    all_courses_list = []

    raw_course_list = course_read_line.replace(" ", "").replace("\n", "").split(",")
    for course_raw_str in raw_course_list:
        for i in range(len(course_raw_str)):
            if course_raw_str[i].isdigit():  # i is now the index of first digit
                fac = course_raw_str[:i]  # faculty
                uid = course_raw_str[i:]  # course uni id num thing
                all_courses_list.append(ACourse(fac, uid))
                break  # yes i have reached that level now
    return all_courses_list


def __optimize_end_early(option, best_case_option):
    """
    :param option:
    :param best_case_option:
    :return:
    the best option with the earliest end times
    """
    best_case_week = [[], [], [], [], [], [], []]
    for class_obj in best_case_option:
        for inner_tuple in class_obj.class_time.time_list:
            if not isinstance(best_case_week[inner_tuple[1].weekday()], datetime) or \
                    best_case_week[inner_tuple[1].weekday()] < inner_tuple[1]:  # more recent in time
                best_case_week[inner_tuple[1].weekday()] = inner_tuple[1]

    this_case_week = [[], [], [], [], [], [], []]
    for class_obj in option:
        for inner_tuple in class_obj.class_time.time_list:
            if not isinstance(this_case_week[inner_tuple[1].weekday()], datetime) or \
                    this_case_week[inner_tuple[1].weekday()] < inner_tuple[1]:  # more recent in time
                this_case_week[inner_tuple[1].weekday()] = inner_tuple[1]

    best_case_delta = datetime(1, 1, 1, 0, 0)
    this_case_delta = datetime(1, 1, 1, 0, 0)
    for day_i in range(7):
        tester = datetime(this_case_week[day_i].year, this_case_week[day_i].month, this_case_week[day_i].day, 0, 0)
        best_case_delta += best_case_week[day_i] - tester

        tester = datetime(this_case_week[day_i].year, this_case_week[day_i].month, this_case_week[day_i].day, 0, 0)
        this_case_delta += this_case_week[day_i] - tester

        if this_case_delta > best_case_delta:  # the greater the delta, the later classes end, return smallest delta
            return best_case_option
        else:
            return option


def __optimize_day_off(option, best_case_option, int_day_off):
    """
    :param option:
    :param best_case_option:
    :param int_day_off:
    Monday = 0, Tuesday = 1, Wednesday = 2, Thursday = 3, Friday = 4, Saturday = 5, Sunday = 6
    :return:
    the option with the most days off
    """
    weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    if isinstance(int_day_off, str):
        if int_day_off.lower() in weekdays:
            int_day_off = weekdays.index(int_day_off.lower())
        else:
            raise ValueError

    elif isinstance(int_day_off, int) and 0 <= int_day_off <= 6:
        best_day = []
        for class_obj in best_case_option:
            for inner_tuple in class_obj.class_time.time_list:
                if inner_tuple[0].weekday() == int_day_off:
                    best_day.append(inner_tuple)

        this_day = []
        for class_obj in option:
            for inner_tuple in class_obj.class_time.time_list:
                if inner_tuple[0].weekday() == int_day_off:
                    this_day.append(inner_tuple)

        best_case_delta = datetime(1, 1, 1, 0, 0)  # deltas represent total class time on the int_day_off
        for element in best_day:
            start = datetime(1, 1, 1, element[0].hour, element[0].second)
            end = datetime(1, 1, 1, element[1].hour, element[1].second)
            best_case_delta += end - start

        this_case_delta = datetime(1, 1, 1, 0, 0)  # deltas represent total class time on the int_day_off
        for element in this_day:
            start = datetime(1, 1, 1, element[0].hour, element[0].second)
            end = datetime(1, 1, 1, element[1].hour, element[1].second)
            this_case_delta += end - start

            if best_case_delta < this_case_delta:  # return smallest delta
                return best_case_option
            else:
                return option
    else:
        raise TypeError


def __print_class_info(class_obj):
    """
    Ripped the code from CourseStructure.py, for some reason I cant call the class's methods?
    :param class_obj:
    :return:
    """
    pass
    """class_time_str = ""
    obj_time_list = class_obj.class_time.time_list
    for datetime_tuple in obj_time_list:
        start_time = datetime_tuple[0]
        end_time = datetime_tuple[1]
        class_time_str += "@" + str(start_time) + "~" + str(end_time)
        if obj_time_list.index(datetime_tuple) != len(obj_time_list) - 1:
            class_time_str += ", "

    return ("Course=" + str(class_obj.fac) + " " + str(class_obj.uid) + "\n" +
            "CRN=" + str(class_obj.crn) + "\n" +
            "Title=" + str(class_obj.title) + "\n" +
            "Type=" + str(class_obj.class_type) + "\n" +
            "Section=" + str(class_obj.section) + "\n" +
            "Time=" + class_time_str + "\n" +
            "Seats=" + str(class_obj.seats) + "\n" +
            "Instruction=" + str(class_obj.instruction) + "\n" +
            "Campus=" + str(class_obj.campus) + "\n" +
            "Building=" + str(class_obj.building) + "\n" +
            "Room=" + str(class_obj.room) + "\n")"""
