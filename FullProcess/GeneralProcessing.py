from COREClassStructure.CourseClassStructure import ACourse
from COREClassStructure.TermScheduleStructure import TermSchedule
from COREDB.ClassPull import pull_class_object_list_via, classes_from_course_count
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
        try:
            new_course_obj = ACourse(combined=possible_course)  # Validation done far in backend at ACourse
            all_courses_list.append(new_course_obj)
        except Exception as e:
            raise e

    return all_courses_list


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


def raise_value_error_for_unknown_course_on_db(course_objects_list):
    """
    Void function, raises a ValueError for an unknown course not listed on the DB
    :param course_objects_list:
    List -> List of ACourse objects
    """
    for course_object in course_objects_list:
        if not isinstance(course_object, ACourse):
            raise TypeError(course_object)

        if classes_from_course_count(course_object) <= 0:
            raise ValueError(f"Unknown Course: '{course_object.get_raw_str()}'\n"
                             f"Please send a course update request if needed")
