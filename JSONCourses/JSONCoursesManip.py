import json
import jsonpickle

from Scaper.Scraper import scrape_course_class_objs


def __write_class_objs(file_name, class_obj_list):
    file_name = file_name if file_name[-5:] == ".json" else file_name + ".json"  # ensure .txt file type

    encoded = jsonpickle.encode(class_obj_list, unpicklable=False)

    with open(file_name, 'w') as f:  # with open("JSONCourses/" + file_name, 'w') as f:
        json.dump(encoded, f, indent=4)

        print("\tSuccessfully created Schedule raw CRN data file:", file_name)


def update_course_json(course_obj_list):
    for course_obj in course_obj_list:
        class_obj_list = scrape_course_class_objs(course_obj)  # scrape all classes per course
        __write_class_objs((course_obj.fac + course_obj.uid), class_obj_list)


"""
Test Code
"""
from ClassStructure.CourseStructure import ACourse

update_course_json([ACourse(fac="COMM", uid="1050U")])
