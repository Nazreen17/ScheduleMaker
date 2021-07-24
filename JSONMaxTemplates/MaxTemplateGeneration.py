#!/usr/bin/env python

import time

from ClassStructure.MaxTemplateStructure import MaxTemplate
from ClassStructure.FlipClock import FlipClock
from DB.SQLCoursePullController import pull_class


def generate(course_obj_list):
    start = time.time()

    courses_2d_list = []

    for course_obj in course_obj_list:
        courses_2d_list.append(pull_class(course_obj.fac, course_obj.uid))
    courses_2d_list = __cut(courses_2d_list)
    # now courses_2d_list = [[AClass list from Course 1], [AClass list from Course 2], etc], 0 seats left removed/cut

    main_schedules_list = __flip_clock_combinations(courses_2d_list)
    print(f"\tGenerated {len(main_schedules_list)} CRN simplified schedules ({str(round(time.time() - start, 2))} sec)")

    main_schedules_list = __crn_clean_up(main_schedules_list)
    # converting MaxSchedule to a clear list of CRN codes

    return main_schedules_list


def __crn_clean_up(main_schedules_list):
    extracted_crn = []
    for max_schedule_obj in main_schedules_list:
        extracted_crn.append(max_schedule_obj.crn_list)
    return extracted_crn


def __cut(courses_2d_list):
    for course_list in courses_2d_list:
        for class_obj in course_list:
            if class_obj.seats == 0:
                course_list.remove(class_obj)
    return courses_2d_list


def __flip_clock_combinations(courses_2d_list):
    all_combinations = []
    clock = FlipClock(courses_2d_list)

    print(f"\tMaximum {str(clock.shift_max)} possible flip clock combinations")

    for shift_count in range(clock.shift_max):
        temp_schedule = MaxTemplate()
        loop_continue = True
        inner_list_index = 0
        while loop_continue:
            if loop_continue and inner_list_index < len(courses_2d_list):
                temp_schedule.add_from_class(courses_2d_list[inner_list_index][clock[inner_list_index]])
                inner_list_index += 1
                if temp_schedule.is_valid() is False:
                    loop_continue = False
            else:
                loop_continue = False
                all_combinations.append(temp_schedule)
        clock.shift()  # shift late, clock starts a 0 which is possibly valid
    return all_combinations
