import itertools
import os
from multiprocessing import Process, Lock, Manager

from constants import MAX_COURSE_COMBOS, SINGLE_PROCESS_COMBOS
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

    # 3) Compute all combinations of options through conversion of all CRN code based options to class objects
    main_schedules_list = __compute_all_combinations(list_3d, valid_courses_list_2d)

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
    all_combos = list(itertools.product(*list_3d))  # Generate all combos

    processes = []  # Multi process list
    cpu_core_count = os.cpu_count()  # Number of CPUs on the machine
    lock = Lock()  # Lock to prevent race condition

    with Manager() as manager:
        verified_combos = manager.list()

        if len(all_combos) > MAX_COURSE_COMBOS:
            raise RuntimeError(f"Surpassed MAX_COURSE_COMBOS = {MAX_COURSE_COMBOS} <  {len(all_combos)}")

        process_count = len(all_combos) // SINGLE_PROCESS_COMBOS
        process_count += 1 if len(all_combos) % SINGLE_PROCESS_COMBOS != 0 else 0

        for i in range(process_count):
            if i < process_count - 1:  # Not the last process
                new_process = Process(target=__single_process_validation,
                                      args=(lock,
                                            all_combos[i * SINGLE_PROCESS_COMBOS:(i + 1) * SINGLE_PROCESS_COMBOS],
                                            verified_combos, valid_courses_list_2d))
            else:  # Last process
                new_process = Process(target=__single_process_validation,
                                      args=(lock, all_combos[i * SINGLE_PROCESS_COMBOS:], verified_combos,
                                            valid_courses_list_2d))

            processes.append(new_process)

        if len(processes) > cpu_core_count:
            print(f"\tWARNING! Processes created: {process_count} | CPU core count: {cpu_core_count}")

        for process in processes:  # Start all processes
            process.start()

        for process in processes:  # Wait for all processes to finish
            process.join()

        return list(verified_combos)


def __single_process_validation(lock, all_combos, verified_combos, valid_courses_list_2d):
    for combo in all_combos:
        possible_valid_crn_combo = list(itertools.chain(*combo))  # Merge 4D list ->
        # Each 4th dimension lists a course sublist of a max combo option

        pulled_class_from_possible = __find_from_crn_list(possible_valid_crn_combo, valid_courses_list_2d)

        if TermSchedule(pulled_class_from_possible).is_time_valid():  # Verify time validation with TermSchedule
            lock.acquire()  # Lock non local all_combos_array
            verified_combos.append(possible_valid_crn_combo)  # Add the completed schedule
            lock.release()  # Unlock non local all_combos_array


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
