def schedules_read(file_name):
    file_name = file_name if file_name[-4:] == ".txt" else file_name + ".txt"  # ensure .txt file type

    try:
        with open("DBv1Schedules/" + file_name, "r") as f:
            read_text = f.readlines()
            f.close()
        return read_text
    except FileNotFoundError:
        raise FileNotFoundError(file_name, "does not exist!")


def schedules_write(file_name, all_schedules_list, courses_list):
    file_name = file_name if file_name[-4:] == ".txt" else file_name + ".txt"  # ensure .txt file type

    data = ""

    for course in courses_list:
        data += str(course.fac) + str(course.uid)
        if courses_list.index(course) + 1 != len(courses_list):
            data += ", "
    data += "\n"

    for course_option_i in range(len(all_schedules_list)):
        spacing = ")\t\t" if (course_option_i + 1) < 100 else ")\t"
        data += str(course_option_i + 1) + spacing + str(all_schedules_list[course_option_i]) + "\n"

    with open("DBv1Schedules/" + str(file_name), "w") as f:
        f.write(data)
        f.close()
        print("\tSuccessfully created Schedule raw CRN data file:", file_name)
