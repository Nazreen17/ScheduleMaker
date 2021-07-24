#!/usr/bin/env python

import time

from ClassStructure.MaxTemplateStructure import MaxTemplate
from ClassStructure.FlipClock import FlipClock
from DB.SQLCoursePullController import pull_class


def generate(course_obj_list):
    start = time.time()

    list_3d = []
    # First dimension element = general list of all courses
    # Second dimension element = single course list of all its options
    # Third dimension element = a single option of the parent course

    all_course_classes = []

    for course_obj in course_obj_list:
        all_course_classes.append(pull_class(fac=course_obj.fac, uid=course_obj.uid, seats=1))  # Pull all classes

    for course_sublist in all_course_classes:  # Cycle through each course sublist to compute in 2d list format
        course_2d_sublist = []

        for class_obj in course_sublist:  # Cycle all class objects
            if class_obj.class_type == "Lecture":

                if len(class_obj.links) > 0:  # The lecture class has at least 1 linked secondary class option
                    for found_option_list in class_obj.links:  # Loop through each lecture's linked options
                        option = [class_obj.crn] + found_option_list  # Create a combined option list
                        course_2d_sublist.append(option)  # Add the combined option list to the course 2d list

                else:  # The lecture class has no linked secondary class options
                    course_2d_sublist.append([class_obj.crn])  # Add the single lecture type to the course 2d list

            list_3d.append(course_2d_sublist)
    # Example list_3d =
    # [
    #  [ [Course 1, Option 1 CRN Codes], [Course 1, Option 2 CRN Codes] ],
    #  [ [Course 2, Option 1 CRN Codes], [Course 2, Option 2 CRN Codes], [Course 2, Option 3 CRN Codes] ],
    # ... etc
    # ]

    main_schedules_list = __flip_clock_combinations(list_3d, all_course_classes)
    print(f"\tGenerated {len(main_schedules_list)} CRN simplified schedules ({str(round(time.time() - start, 2))} sec)")

    main_schedules_list = __crn_clean_up(main_schedules_list)  # converting MaxSchedule to a clear list of CRN codes

    return main_schedules_list


def __flip_clock_combinations(list_3d, all_course_classes):
    all_combinations = []
    clock = FlipClock(list_3d)

    print(f"\tMaximum {str(clock.shift_max)} possible flip clock combinations")

    for shift_count in range(clock.shift_max):  # loop for max shifts possible
        temp_schedule = MaxTemplate()
        loop_continue = True
        course_index = 0
        while loop_continue:  # Loop through all courses
            if loop_continue and course_index < len(list_3d):  # Still classes left to check
                current_course_option_i = clock[course_index]  # Get the current option
                temp_schedule.add_from_class(list_3d[course_index][current_course_option_i])  # add classes from option
                course_index += 1  # Shift to next class object
            else:  # Done class class looping
                loop_continue = False
                all_combinations.append(temp_schedule)  # Add the completed schedule
                # TODO !!!!!!!!!! ADD is_valid CONTROL !!!!!!!!!!
        clock.shift()  # shift late, clock starts a 0 which is possibly valid
    return all_combinations


def __find_from_crn(crn, all_course_classes):
    """
    :param crn:
    INT crn code
    :param all_course_classes:
    List of all classes in 3d organized format
    :return:
    Return a class object with matching crn, or None if no match was found
    """
    for course_sublist in all_course_classes:
        for class_object in course_sublist:
            if class_object.crn == crn:
                return class_object
    return None


def __crn_clean_up(main_schedules_list):
    extracted_crn = []
    for max_schedule_obj in main_schedules_list:
        extracted_crn.append(max_schedule_obj.crn_list)
    return extracted_crn
