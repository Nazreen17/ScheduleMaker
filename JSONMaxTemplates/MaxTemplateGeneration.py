#!/usr/bin/env python

import time

from ClassStructure.TermScheduleStructure import TermSchedule
from ClassStructure.MaxTemplateStructure import MaxTemplate
from ClassStructure.FlipClock import FlipClock
from DB.SQLCoursePullController import pull_class


def generate(course_obj_list):
    start = time.time()

    list_3d = []
    # First dimension element = general list of all courses
    # Second dimension element = single course list of all its options
    # Third dimension element = a single option of the parent course

    for course_obj in course_obj_list:
        lectures_list = pull_class(fac=course_obj.fac, uid=course_obj.uid, class_type="Lecture", seats=1)

        course_options = []

        for lecture_obj in lectures_list:
            for option_list in lecture_obj.links:  # Loop through each lecture's linked options
                temp_option_list = [lecture_obj]

                for link_crn in option_list:  # Loop through each crn code in the linked option
                    temp_option_list += pull_class(fac=lecture_obj.fac, uid=lecture_obj.uid, seats=1, crn=link_crn)

                if TermSchedule().add_class(temp_option_list).is_valid():
                    # TODO WHYYYYYYYYYYYYYdddddyyyyy
                    course_options.append(temp_option_list)

        list_3d.append(course_options)
    # Example list_3d =
    # [
    #  [ [Course 1, Option 1 Classes], [Course 1, Option 2 Classes] ],
    #  [ [Course 2, Option 1 Classes], [Course 2, Option 2 Classes], [Course 2, Option 3 Classes] ],
    # ... etc
    # ]

    main_schedules_list = __flip_clock_combinations(list_3d)
    print(f"\tGenerated {len(main_schedules_list)} CRN simplified schedules ({str(round(time.time() - start, 2))} sec)")

    main_schedules_list = __crn_clean_up(main_schedules_list)
    # converting MaxSchedule to a clear list of CRN codes

    return main_schedules_list


def __flip_clock_combinations(list_3d):
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
        clock.shift()  # shift late, clock starts a 0 which is possibly valid
    return all_combinations


def __crn_clean_up(main_schedules_list):
    extracted_crn = []
    for max_schedule_obj in main_schedules_list:
        extracted_crn.append(max_schedule_obj.crn_list)
    return extracted_crn
