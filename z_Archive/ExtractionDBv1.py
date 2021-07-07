from Structure.CourseStructure import LinkOption, Lecture, Secondary
from Structure.TimeStructure import ClassTime
from DBv1Courses.DBv1CoursesFileManip import courses_read

from datetime import datetime


def extract(all_courses_list):
    """
    extract all classes related to a list of ACourse objects
    :return:
    return [[Class objects from Course 1], [Class objects from Course 2], etc]
    """
    total_extracted_course_list = []

    for course_obj in all_courses_list:
        data = courses_read(course_obj.fac + course_obj.uid)
        class_count = len(data) // 13
        extracted_classes_list = []
        for i in range(class_count):
            fac = course_obj.fac
            uid = course_obj.uid
            extracted_class = __extract_class(data, fac, uid)
            if extracted_class.seats != 0:
                extracted_classes_list.append(extracted_class)
            data = data[13:]
        total_extracted_course_list.append(extracted_classes_list)

    return total_extracted_course_list


def __extract_class(data, fac, uid):
    """
    :param data:
    :param fac:
    :param uid:
    :return:
    Lecture and Secondary objects from data on DBv1Courses
    """
    crn = int(__clean_up(data[1]))
    title = __clean_up(data[2])
    class_type = __clean_up(data[3])
    section = int(__clean_up(data[4]))
    class_time = __class_time(__clean_up(data[5]))
    links = __links(__clean_up(data[6]))
    seats = int(__clean_up(data[7]))
    instruction = __clean_up(data[8])
    campus = __clean_up(data[9])
    building = __clean_up(data[10])
    room = __clean_up(data[11])
    """
    ^^^ This method is so incredibly stupid since its using index values on a text file which is saved by me.
    BUT, it works so ...
    """

    if data[12] != "\n":
        raise ValueError("Something went wrong with DBv1Courses class extraction")

    if class_type == "Lecture":
        return Lecture(fac, uid, crn, title, class_type, section, class_time, links, seats, instruction, campus,
                       building, room)
    elif class_type == "Laboratory" or class_type == "Tutorial":
        return Secondary(fac, uid, crn, title, class_type, section, class_time, links, seats, instruction,
                         campus, building, room)


def __clean_up(line):
    """
    :param line:
    :return:
    return cleaned up data from str line
    example: CRN=12345\n -> returns "12345"
    """
    return line[line.index("=") + 1:].replace("\n", "")


def __links(db_text):
    """
    :param db_text:
    :return:
    returns a LinkOptions object using DBv1Courses text
    """
    options = []
    while True:
        try:
            option_text = db_text[db_text.index("[") + 1:db_text.index("]")]
            links = list(map(int, option_text.split(", ")))
            db_text = db_text[len(option_text) + 2:]  # + 2 accounts for the "[" and "]"
            options.append(links)
        except ValueError:  # end of all options (no longer can find index of "[")
            if len(options) > 0:
                return LinkOption(options)
            else:
                return


def __class_time(db_text):
    """
    :param db_text:
    :return:
    returns a ClassTime object using DBv1Courses text
    """
    time_list = []
    while True:
        try:
            start_text = db_text[db_text.index("@") + 1:db_text.index("~")]
            db_text = db_text[db_text.index("~"):]
            start = datetime.strptime(start_text, '%Y-%m-%d %H:%M:%S')
            try:
                end_text = db_text[db_text.index("~") + 1:db_text.index(",")]
                db_text = db_text[db_text.index(","):]
                end = datetime.strptime(end_text, '%Y-%m-%d %H:%M:%S')
                if len(time_list) > 0:
                    if __is_biweekly(time_list[-1], (start, end)) is False:  # ensure the time_list is not biweekly
                        time_list.append((start, end))
                else:
                    time_list.append((start, end))
            except ValueError:  # end of ClassTime data
                end_text = db_text[db_text.index("~") + 1:]
                end = datetime.strptime(end_text, '%Y-%m-%d %H:%M:%S')
                if len(time_list) > 0:
                    if __is_biweekly(time_list[-1], (start, end)) is False:  # ensure the time_list is not biweekly
                        time_list.append((start, end))
                else:
                    time_list.append((start, end))
                return ClassTime(time_list)
        except ValueError:  # end of all options (no longer can find index of "[")
            return ClassTime(time_list)


def __is_biweekly(last_tuple, current_tuple):
    """
    is_biweekly includes all datetimes that have the same weekday (Mon, Tue, Wed, etc) and same times.
    This prevents logical time conflicts since the program will believe there are 2 (or more) class times that start and
    end at the same time on the same weekday.
    :param last_tuple:
    :param current_tuple:
    :return:
    True or False determining if a course has biweekly times
    """
    if (last_tuple[0].weekday() == current_tuple[0].weekday() and last_tuple[0].time() == current_tuple[0].time()) and \
            (last_tuple[1].weekday() == current_tuple[1].weekday() and last_tuple[1].time() == current_tuple[1].time()):
        return True
    else:
        return False
