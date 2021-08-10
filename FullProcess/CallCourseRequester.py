from COREDB.RequestCourseUpdate import add_course_request, remove_request
from COREDB.RequestCoursePull import read_all_course_request_as_list


def add_course_requests_via_list(courses_list):
    """
    :param courses_list:
    list -> str or ACourse -> Defines the courses to add (Validation is done further on back end)
    """
    for course in courses_list:
        add_course_request(course)


def drop_course_requests_via_list(courses_list):
    """
    :param courses_list:
    list -> str or ACourse -> Defines the courses to add (Validation is done further on back end)
    """
    for course in courses_list:
        remove_request(course)


def pull_course_requests_as_str():
    """
    :return:
    Returns a str of course_requests
    """
    details_list = read_all_course_request_as_list()

    return_str = ""
    for detail in details_list:
        return_str += (f"Course: {detail[0]}\n"
                       f"Updated: {detail[1].strftime('%Y/%m/%d %H:%M:%S')}\n\n")

    return_str += "" if len(return_str) > 0 else "No Request details found"

    return return_str
