import itertools

from COREClassStructure.TermScheduleStructure import TermSchedule
from COREDB.ClassPull import pull_class_object_list_via


def generate(course_obj_list):
    """
    :param course_obj_list:
    LIST of course objects
    :return:
    Returns a list of CRN codes representing all possible schedule combinations with valid seats and time conflict free.
    """
    valid_courses_list_2d = []

    # 1) Pull all classes you consider valid into valid_courses_list_2d (No time conflict computation yet)
    for course_obj in course_obj_list:
        valid_courses_list_2d.append(pull_class_object_list_via(fac=course_obj.fac, uid=course_obj.uid, seats=1))
        # WARNING! ONLY PULL CLASSES DEEMED VALID INTO valid_courses_list_2d!
        #  LESS OVERHEAD AND REQUIRED FOR MaxSchedule VALIDATION!

    # 2) Compute all possible options based on links of lecture type classes
    list_3d = __compute_options(valid_courses_list_2d)
    # First dimension element = general list of all courses
    # Second dimension element = single course list of all its options
    # Third dimension element = a single option of the parent course

    # 3) Compute all combinations of options through conversion of all CRN code based options to class objects,
    # is_time_valid() processing also takes place here
    main_schedules_list = __compute_all_combinations(list_3d, valid_courses_list_2d)

    """
    # 4) Convert all objects to CRN codes to easier printing
    main_schedules_list = __crn_clean_up(main_schedules_list)  # converting MaxSchedule to a clear list of CRN codes
    """

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


def __compute_all_combinations(list_3d, valid_courses_list_2d):
    """
    Runs all possible combinations of course options and checks for time conflicts
    :param list_3d:
    :param valid_courses_list_2d:
    List of all classes in 2D organized format
    :return:
    """
    verified_combos = []
    all_combos = list(itertools.product(*list_3d))

    for combo in all_combos:
        possible_valid_crn_combo = list(itertools.chain(*combo))
        if __is_valid_crn_options(possible_valid_crn_combo, valid_courses_list_2d):
            # Verify the class was pulled originally and deemed valid

            pulled_class_from_possible = __find_from_crn_list(possible_valid_crn_combo, valid_courses_list_2d)
            if TermSchedule(pulled_class_from_possible).is_time_valid():
                # Verify time validation with TermSchedule
                verified_combos.append(possible_valid_crn_combo)
        # Merge 4D list -> Each 4th dimension lists a course sublist of a max combo option
    return verified_combos


def __is_valid_crn_options(crn_list, valid_courses_list_2d):
    """
    Copied core logic from __find_from_crn_list()
    :param crn_list:
    List of crn codes to search
    :param valid_courses_list_2d:
    List of all classes in 2D organized format
    :return:
    Return BOOL True or False to determine if CRN list is a valid option
    """
    temp_crn_list = crn_list.copy()  # Always copy lists when applying functions like .remove() which is done here below

    for course_sublist in valid_courses_list_2d:
        if len(temp_crn_list) > 0:
            for class_object in course_sublist:
                if class_object.crn in temp_crn_list:
                    temp_crn_list.remove(class_object.crn)  # Remove the crn code that was found
                elif len(temp_crn_list) == 0:  # No more crn codes to search
                    return True
        if len(temp_crn_list) == 0:  # No more crn codes to search, control for the very last class in list_2d
            return True

    return False


def __find_from_crn_list(crn_list, valid_courses_list_2d):
    """
    :param crn_list:
    List of crn codes to search
    :param valid_courses_list_2d:
    List of all classes in 2d organized format
    :return:
    Return a list of class object with matching crn
    """
    class_objects_list = []
    temp_crn_list = crn_list.copy()  # Always copy lists when applying functions like .remove() which is done here below

    for course_sublist in valid_courses_list_2d:
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
    for term_schedule_object in main_schedules_list:
        crn_code_list = []
        for class_object in term_schedule_object.classes:
            crn_code_list.append(class_object.crn)
        extracted_crn.append(crn_code_list)
    return extracted_crn
