import time

from Scaper.Scraper import scrape_course_class_objs


def courses_read(file_name):
    """
    :param file_name:
    :return:
    returns a list of strings, each index element is a line of file_name.txt from DBv1Courses
    """
    file_name = file_name if file_name[-4:] == ".txt" else file_name + ".txt"  # ensure .txt file type

    try:
        with open("DBv1Courses/" + file_name, "r") as f:
            read_text = f.readlines()
            f.close()
        return read_text
    except FileNotFoundError:
        raise FileNotFoundError(file_name, "does not exist!")


def courses_write(file_name, add_data):
    """
    writes add_data to file_name.txt from DBv1Courses (overwrites all previous data in the .txt)
    :param file_name:
    :param add_data:
    :return:
    no return
    """
    file_name = file_name if file_name[-4:] == ".txt" else file_name + ".txt"  # ensure .txt file type

    with open("DBv1Courses/" + file_name, "w") as f:
        f.write(add_data)
        f.close()


def update_course_file(courses_list):
    """
    main function used to update a course file, calls a menu requesting user inputs of course names.
    once course names are obtained, the final result is a .txt file storing all the course's classes' information
    :return:
    no return
    """
    all_courses_list = courses_list

    for course in all_courses_list:
        write_data = ""
        class_read_execution_start = time.time()
        course_classes_list = scrape_course_class_objs(course)  # scrape all classes per course
        for class_obj in course_classes_list:
            write_data += class_obj.get_raw_str()
            courses_write((course.fac + course.uid), write_data)
        print("\tUpdated:", str(course.uid) + str(course.fac) + ".txt")
        print("\tCourse", str(course.uid) + str(course.fac), "took:",
              str(round(time.time() - class_read_execution_start, 2)) + "sec")
