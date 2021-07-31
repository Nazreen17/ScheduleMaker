from COREClassStructure.CourseClassStructure import ACourse
from Optimizations.EndEarly import EndEarly
from Optimizations.OffDays import OffDay


def get_clean_courses_list(course_bot_input):
    """
    :param course_bot_input:
    STR Course inputs or a single Course input (Math1010U MATH 1010 U, etc) all auto corrected here
    :return:
    A list of Course objects
    """
    all_courses_list = []

    course_bot_input = course_bot_input.lower().replace(" ", "")  # Lower case and remove spaces
    course_bot_input = course_bot_input.translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\\|`~-=_+"})
    # Remove all special characters

    course_str_list = []
    i = 1
    while len(course_bot_input) > 1:
        if course_bot_input[i] == "u" and course_bot_input[i - 1].isdigit():  # Isolate the end of a uid to split by
            course_str_list.append(course_bot_input[:i + 1])  # Find and save course substring into list (+1 for 'u')
            course_bot_input = course_bot_input[i + 1:]  # Again, +1 for the 'u'
            i = 1  # Reset the iterator (since we removed the front end course, gotta start from beginning again)
        else:
            i += 1  # No uid ending 'u' found, increase the character shift iterator by 1 to check next character

    for possible_course in course_str_list:
        new_course_obj = __get_course_obj(possible_course)

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


def get_optimizers_list():
    return [EndEarly(), OffDay()]
