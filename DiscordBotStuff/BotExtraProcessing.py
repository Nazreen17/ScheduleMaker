#!/usr/bin/env python

from ClassStructure.CourseClassStructure import ACourse


def get_clean_courses_list(course_bot_input):
    """
    :param course_bot_input:
    A List/Tuple of Course inputs or a single Course input (Math1010u, MATH 1010 U, etc) all auto corrected later
    :return:
    A list of Course objects
    """
    all_courses_list = []

    if not isinstance(course_bot_input, list) and not isinstance(course_bot_input, tuple):
        course_bot_input = [course_bot_input]

    for possible_course in course_bot_input:
        new_course_obj = __get_course_obj(possible_course.lower().replace(" ", ""))

        if isinstance(new_course_obj, ACourse) and new_course_obj.is_format_valid() is True:
            all_courses_list.append(new_course_obj)

    return all_courses_list


def __get_course_obj(new_course):
    for i in range(len(new_course)):
        if new_course[i].isdigit():  # i is now the index of first digit
            fac = new_course[:i]  # faculty
            uid = new_course[i:]  # course uni id num thing
            return ACourse(fac, uid)
    return None  # No valid course
