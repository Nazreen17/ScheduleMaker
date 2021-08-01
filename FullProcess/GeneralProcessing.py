from COREClassStructure.CourseClassStructure import ACourse
from COREClassStructure.TermScheduleStructure import TermSchedule
from COREDB.ClassPull import pull_class_object_list_via
from DiscordBotStuff.PNGMaker.Pillow import draw_png_schedule


def get_clean_courses_list(course_inputs):
    """
    :param course_inputs:
    STR Course inputs or a single Course input Example: "Math1010U, %! MATH 1010 U" -> all auto corrected here
    :return:
    A list of Course objects
    """
    all_courses_list = []

    course_inputs = course_inputs.lower().replace(" ", "")  # Lower case and remove spaces
    course_inputs = course_inputs.translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\\|`~-=_+"})
    # Remove all special characters

    course_str_list = []
    i = 1
    while len(course_inputs) > 1:
        if course_inputs[i] == "u" and course_inputs[i - 1].isdigit():  # Isolate the end of a uid to split by
            course_str_list.append(course_inputs[:i + 1])  # Find and save course substring into list (+1 for 'u')
            course_inputs = course_inputs[i + 1:]  # Again, +1 for the 'u'
            i = 1  # Reset the iterator (since we removed the front end course, gotta start from beginning again)
        else:
            i += 1  # No uid ending 'u' found, increase the character shift iterator by 1 to check next character

    for possible_course in course_str_list:
        new_course_obj = __make_course_obj(possible_course)

        if isinstance(new_course_obj, ACourse) and new_course_obj.is_format_valid() is True:
            all_courses_list.append(new_course_obj)
        else:
            raise ValueError(f"{possible_course} is not a valid ACourse object or has incorrect format")

    return all_courses_list


def __make_course_obj(new_course):
    for i in range(len(new_course)):
        if new_course[i].isdigit():  # i is now the index of first digit
            fac = new_course[:i]  # faculty
            uid = new_course[i:]  # course uni id num thing
            return ACourse(fac, uid)
    return None  # No valid course


def make_term_schedule_from_crn_no_overhead(crn_list):
    class_objects_list = []

    for crn in crn_list:
        class_objects_list += pull_class_object_list_via(crn=crn)

    return TermSchedule(class_objects_list)


def generate_png_and_txt(single_term_schedule, result_txt_header_str=None):
    # Generate schedule.png
    draw_png_schedule(single_term_schedule)

    header = f"{result_txt_header_str}\n------------------------------\n" if result_txt_header_str is not None else ""

    # Generate results.txt
    with open("DiscordBotStuff/result.txt", "w") as file:
        file.write(header + single_term_schedule.get_raw_str())
