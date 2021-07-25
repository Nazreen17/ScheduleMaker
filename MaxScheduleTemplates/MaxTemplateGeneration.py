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

    valid_courses_list_2d = []

    # 1) Pull all classes you consider valid into valid_courses_list_2d (No time conflict computation yet)
    for course_obj in course_obj_list:
        valid_courses_list_2d.append(pull_class(fac=course_obj.fac, uid=course_obj.uid, seats=1))  # Pull all classes
        # TODO WARNING! ONLY PULL CLASSES DEEMED VALID! LESS OVERHEAD AND REQUIRED FOR MaxTemplate VALIDATION!

    # 2) Compute all possible options based on links of lecture type classes
    list_3d = __compute_options(valid_courses_list_2d)
    # First dimension element = general list of all courses
    # Second dimension element = single course list of all its options
    # Third dimension element = a single option of the parent course

    # 3) Compute all combinations of options through conversion of all CRN code based options to class objects,
    # is_time_valid() processing also takes place here
    main_schedules_list = __flip_clock_combinations(list_3d, valid_courses_list_2d)

    # 4) Convert all objects to CRN codes to easier printing
    main_schedules_list = __crn_clean_up(main_schedules_list)  # converting MaxSchedule to a clear list of CRN codes

    # 5) Print detailed stats on computation
    print(f"\tGenerated {len(main_schedules_list)} CRN simplified schedules ({str(round(time.time() - start, 2))} sec)")

    return main_schedules_list


def __compute_options(valid_courses_list_2d):
    list_3d = []

    for course_sublist in valid_courses_list_2d:  # Cycle through each course sublist to compute in 2d list format
        course_2d_sublist = []

        for class_obj in course_sublist:  # Cycle all class objects
            if class_obj.class_type == "Lecture":

                if len(class_obj.links) > 0:  # The lecture class has at least 1 linked secondary class option
                    for found_option_list in class_obj.links:  # Loop through each lecture's linked options
                        option = [class_obj.crn] + found_option_list  # Create a combined option list
                        if __is_valid_crn_options(found_option_list, valid_courses_list_2d):
                            # Determine if option course was pulled
                            course_2d_sublist.append(option)  # Add the combined option list to the course 2d list

                else:  # The lecture class has no linked secondary class options
                    course_2d_sublist.append([class_obj.crn])  # Add the single lecture type to the course 2d list

        if len(course_2d_sublist) > 0:
            list_3d.append(course_2d_sublist)

    # Now list_3d = (example ->)
    # [
    #  [ [Course 1, Option 1 CRN Codes], [Course 1, Option 2 CRN Codes] ],
    #  [ [Course 2, Option 1 CRN Codes], [Course 2, Option 2 CRN Codes], [Course 2, Option 3 CRN Codes] ],
    # ... etc
    # ]
    return list_3d


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

    for shift_count in range(max_shifting):  # Loop for max shifts possible
        temp_schedule = MaxTemplate()
        loop_continue = True
        course_index = 0

        while loop_continue:  # Loop through all courses
            if loop_continue and course_index < len(list_3d):  # Still classes left to check
                current_course_option_index = clock[course_index]  # Get the current option index from clock
                crn_list = list_3d[course_index][current_course_option_index]  # get the crn list

                converted_to_class_objects = __find_from_crn_list(crn_list, all_course_classes)
                temp_schedule.add_from_class(converted_to_class_objects)

                course_index += 1  # Shift to next course index

            else:  # Finished going through all course
                loop_continue = False  # Break loop

        if len(temp_schedule) > 0 and temp_schedule.is_time_valid():  # Only add if time valid and len is okay
            all_combinations.append(temp_schedule)  # Add the completed schedule

            if max_shifting > MAX_SCHEDULE_COMBINATIONS:
                print(f"\tWARNING! Passed the set max {MAX_SCHEDULE_COMBINATIONS} combinations, returned 1")

                return all_combinations

        clock.shift()  # shift late, clock starts a 0 which is possibly valid
    return all_combinations


def __is_valid_crn_options(crn_list, list_2d):
    """
    Copied core logic from __find_from_crn_list()
    :param crn_list:
    List of crn codes to search
    :param list_2d:
    List of all classes in 3d organized format
    :return:
    Return BOOL True or False to determine if CRN list is a valid option
    """
    temp_crn_list = crn_list.copy()  # Always copy lists when applying functions like .remove() which is done here below

    for course_sublist in list_2d:
        if len(temp_crn_list) > 0:
            for class_object in course_sublist:
                if class_object.crn in temp_crn_list:
                    temp_crn_list.remove(class_object.crn)  # Remove the crn code that was found
                elif len(temp_crn_list) == 0:  # No more crn codes to search
                    return True
        if len(temp_crn_list) == 0:  # No more crn codes to search, control for the very last class in list_2d
            return True

    return False


def __find_from_crn_list(crn_list, list_2d):
    """
    :param crn_list:
    List of crn codes to search
    :param list_2d:
    List of all classes in 3d organized format
    :return:
    Return a list of class object with matching crn
    """
    class_objects_list = []
    temp_crn_list = crn_list.copy()  # Always copy lists when applying functions like .remove() which is done here below

    for course_sublist in list_2d:
        if len(temp_crn_list) > 0:
            for class_object in course_sublist:
                if class_object.crn in temp_crn_list:
                    class_objects_list.append(class_object)
                    temp_crn_list.remove(class_object.crn)  # Remove the crn code that was found
                elif len(temp_crn_list) == 0:  # No more crn codes to search
                    return class_objects_list
        if len(temp_crn_list) == 0:  # No more crn codes to search, control for the very last class in list_2d
            return class_objects_list

    return class_objects_list


def __crn_clean_up(main_schedules_list):
    extracted_crn = []
    for max_schedule_obj in main_schedules_list:
        extracted_crn.append(max_schedule_obj.crn_list)
    return extracted_crn
