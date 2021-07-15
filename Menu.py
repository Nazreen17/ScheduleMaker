#!/usr/bin/env python

from ClassStructure.CourseClassStructure import ACourse
from constants import STOP_CODES


def get_courses_list():
    """
    :return:
    a list of Course objects
    """
    print("\tType in", STOP_CODES, "to stop!")
    all_courses_list = []

    while True:
        new_course_obj = __user_course_input()
        if new_course_obj is None:  # stop code inputted
            return all_courses_list
        if new_course_obj.is_format_valid() is True:
            all_courses_list.append(new_course_obj)
        else:
            print("\tInvalid course name inputted! (Ex: Math 1010U)")


def __user_course_input():
    """
    :return:
    return the Course object of a single course from user input
    """
    new_course = input("Course code (Ex: Math 1010U) > ").replace(" ", "").lower()
    if new_course in STOP_CODES:  # exit code inputted
        return None  # None denotes run

    for i in range(len(new_course)):
        if new_course[i].isdigit():  # i is now the index of first digit
            fac = new_course[:i]  # faculty
            uid = new_course[i:]  # course uni id num thing
            return ACourse(fac, uid)
