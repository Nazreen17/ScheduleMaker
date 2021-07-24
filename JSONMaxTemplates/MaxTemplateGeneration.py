#!/usr/bin/env python

import time

from ClassStructure.MaxTemplateStructure import MaxTemplate
from ClassStructure.FlipClock import FlipClock
from DB.SQLCoursePullController import pull_class
from constants import MAX_SCHEDULE_COMBINATIONS


def generate(course_obj_list):
    """
    :param course_obj_list:
    LIST of course objects
    :return:
    Returns a list of CRN codes representing all possible schedule combinations with valid seats and time conflict free.
    """
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
    """
    Runs all possible combinations of course options and checks for time conflicts
    :param list_3d:
    :param all_course_classes:
    :return:
    """
    all_combinations = []
    clock = FlipClock(list_3d)

    max_shifting = clock.shift_max

    print(f"\tMaximum {str(max_shifting)} possible flip clock combinations")

    for shift_count in range(max_shifting):  # loop for max shifts possible
        temp_schedule = MaxTemplate()
        loop_continue = True
        course_index = 0
        while loop_continue:  # Loop through all courses
            if loop_continue and course_index < len(list_3d):  # Still classes left to check
                current_course_option_index = clock[course_index]  # Get the current option index from clock
                crn_list = list_3d[course_index][current_course_option_index]  # get the crn list

                converted_to_class_objects = __find_from_crn_list(crn_list, all_course_classes)
                temp_schedule.add_from_class(converted_to_class_objects)  # add classes from option

                course_index += 1  # Shift to next course index

            else:  # Finished going through all course
                loop_continue = False
                if len(temp_schedule) > 0 and temp_schedule.is_valid():  # Only add the current max schedule if valid
                    all_combinations.append(temp_schedule)  # Add the completed schedule

                    if max_shifting > MAX_SCHEDULE_COMBINATIONS:
                        print(f"\tWARNING! Passed the set max {MAX_SCHEDULE_COMBINATIONS} combinations, returned 1")
                        # TODO ^^^ Temporary? Return the first valid max schedule when too many combinations possible
                        return all_combinations
        clock.shift()  # shift late, clock starts a 0 which is possibly valid
    return all_combinations


def __find_from_crn_list(crn_list, all_course_classes):
    """
    :param crn_list:
    List of crn codes to search
    :param all_course_classes:
    List of all classes in 3d organized format
    :return:
    Return a list of class object with matching crn
    """
    class_objects_list = []
    temp_crn_list = crn_list.copy()  # Always copy lists when applying functions like .remove() which is done here below

    for course_sublist in all_course_classes:
        if len(temp_crn_list) > 0:
            for class_object in course_sublist:
                if class_object.crn in temp_crn_list and len(temp_crn_list) > 0:
                    class_objects_list.append(class_object)
                    temp_crn_list.remove(class_object.crn)  # Remove the crn code that was found
                elif len(temp_crn_list) == 0:  # No more crn codes to search
                    return class_objects_list
        else:  # No more crn codes to search
            return class_objects_list

    return class_objects_list


def __crn_clean_up(main_schedules_list):
    extracted_crn = []
    for max_schedule_obj in main_schedules_list:
        extracted_crn.append(max_schedule_obj.crn_list)
    return extracted_crn
