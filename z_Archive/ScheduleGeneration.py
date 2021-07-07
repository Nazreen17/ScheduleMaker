from Structure.ScheduleStructure import TermSchedule
from Structure.CourseStructure import Lecture
from Structure.OptimizedOptionStructure import Option
from Structure.FlipClock import FlipClock
from DBv1Courses.ExtractionDBv1 import extract

import time


def generate(courses_list):
    exec_start = time.time()

    print("\t1) Extracting course data...")
    courses_2d_list = extract(courses_list)

    print("\t2) Removing \"0 seat left\" classes...")
    courses_2d_list = __cut(courses_2d_list)
    # courses_2d_list = [[Class objects from Course 1], [Class objects from Course 2], etc], 0 seats left removed/cut

    print("\t3) Converting to options...")
    courses_2d_list = __to_options(courses_2d_list)  # convert courses_2d_list to a list of options by course

    print("\t4) Running matching flip clock combinations...")
    main_schedules_list = __flip_clock_combinations(courses_2d_list).copy()

    print("\t" + str(len(main_schedules_list)), "time valid schedules generated in", str(round(
        time.time() - exec_start, 2)) + "sec")

    return main_schedules_list


def __flip_clock_combinations(courses_2d_list):
    all_combinations = []
    clock = FlipClock(courses_2d_list)

    print("\t\tMaximum", str(clock.shift_max), "possible flip clock combinations")

    for shift_count in range(clock.shift_max):
        temp_schedule = TermSchedule([])
        loop_continue = True
        inner_list_index = 0
        while loop_continue:
            if loop_continue and inner_list_index < len(courses_2d_list):
                temp_schedule.add(courses_2d_list[inner_list_index][clock[inner_list_index]])
                inner_list_index += 1
                if temp_schedule.is_valid() is False:
                    loop_continue = False
            else:
                loop_continue = False
                all_combinations.append(temp_schedule)
        clock.shift()  # shift late, clock starts a 0 which is possibly valid
    return all_combinations


def __to_options(courses_2d_list):
    for course_list_index in range(len(courses_2d_list)):
        temp_options_course = []
        for class_obj in courses_2d_list[course_list_index]:
            if isinstance(class_obj, Lecture):
                if class_obj.links is None:  # lecture type but no links
                    temp_options_course.append(Option(class_obj))
                else:  # lecture type, has links
                    for option_list in class_obj.links.options_list:
                        temp_option = Option(class_obj)
                        expected_links_in_option = len(option_list) + 1
                        for crn in option_list:
                            for class_obj2 in courses_2d_list[course_list_index]:
                                if class_obj2.crn == crn:
                                    temp_option.add(class_obj2)
                        if len(temp_option) == expected_links_in_option:
                            temp_options_course.append(temp_option)

        courses_2d_list[course_list_index] = temp_options_course
    return courses_2d_list


def __cut(courses_2d_list):
    for course_list in courses_2d_list:
        for class_obj in course_list:
            if class_obj.seats == 0:
                course_list.remove(class_obj)
    return courses_2d_list
