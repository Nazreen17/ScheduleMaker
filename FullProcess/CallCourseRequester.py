from COREClassStructure.CourseClassStructure import ACourse
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
