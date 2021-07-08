import json

from Scaper.Scraper import scrape_course_class_objs
from ClassStructure.CourseStructure import AClassDecoder, AClassEncoder


def update_course_json(course_obj_list):
    for course_obj in course_obj_list:
        class_obj_list = scrape_course_class_objs(course_obj)  # scrape all classes per course
        __write_class_objs((course_obj.fac + course_obj.uid), class_obj_list)


def __write_class_objs(file_name, class_obj_list):
    file_name = file_name if file_name[-5:] == ".json" else file_name + ".json"  # ensure .json file type in file_name
    file_name = file_name if file_name[:12] == "JSONCourses/" else "JSONCourses/" + file_name  # ensure proper filepath

    try:
        with open(file_name, "w") as write_file:
            json.dump(class_obj_list, write_file, indent=4, default=AClassEncoder.default)
    except FileNotFoundError:
        with open(file_name[12:], "w") as write_file:
            json.dump(class_obj_list, write_file, indent=4, default=AClassEncoder.default)


def extract_class_list(file_name):
    return __read_class_objs(file_name)


def __read_class_objs(file_name):
    file_name = file_name if file_name[-5:] == ".json" else file_name + ".json"  # ensure .json file type in file_name
    file_name = file_name if file_name[:12] == "JSONCourses/" else "JSONCourses/" + file_name  # ensure proper filepath

    try:
        with open(file_name, "r") as reading_file:
            class_obj_list = json.load(reading_file, cls=AClassDecoder)
    except FileNotFoundError:
        with open(file_name[12:], "r") as reading_file:
            class_obj_list = json.load(reading_file, cls=AClassDecoder)

    return class_obj_list
