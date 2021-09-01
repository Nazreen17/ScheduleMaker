"""
Create a csv file intended to be used as a calendar, generated from a TermSchedule object.
The calendar will avoid a specified exclusion times set by constants.py
"""

import csv
from datetime import datetime, timedelta

from COREClassStructure.TermScheduleStructure import TermSchedule
from constants import CALENDAR_CSV_FILENAME, SEMESTER_EXCLUSION_TIMES, SEMESTER_START, SEMESTER_END
from CacheFilePathManipulation import get_cache_path


def create_csv(term_schedule, user_id=None):
    """
    void -> create a calendar csv file from a TermSchedule
    :param term_schedule:
    TermSchedule -> schedule to convert into a csv calendar
    :param user_id:
    str or int -> identifies user for csv file creation
    """

    # Ensure Object Type
    if not isinstance(term_schedule, TermSchedule):
        raise TypeError(f"Expected TermSchedule type")

    # Header Fields
    fields = ["Subject",
              "Start Date",
              "Start Time",
              "End Date",
              "End Time",
              "Description",
              "Location"]

    # Generating csv Row Data
    row_data_2d = []  # final result must be a 2d list to prevent csv writer error

    if len(term_schedule.classes) == 0:  # if there are no classes ensure 2d list to prevent csv writer error
        row_data_2d = [[]]
    else:  # if there are classes continue as usual
        for a_class in term_schedule.classes:
            row_data_2d += __translate_class_to_lists(a_class)

    # Writing to csv File
    with open(get_cache_path(CALENDAR_CSV_FILENAME, user_id), 'w') as csv_path:
        csv_writer = csv.writer(csv_path)  # create a csv writer object

        csv_writer.writerow(fields)  # writing headers (field names)

        csv_writer.writerows(row_data_2d)  # writing the data rows


def __translate_class_to_lists(a_class):
    """
    :param a_class:
    AClass -> class object from a TermSchedule's classes
    :return:
    list -> of lists of str defining a class object's details
    """
    if a_class.is_biweekly_specific():  # if the class shows biweekly specific behaviour, assume all class times are
        # specified just check for exclusions
        return [__row_event(a_class, meet_time[0], meet_time[1])
                for meet_time in a_class.class_time
                if not __is_exclusion_meet_time(meet_time)]

    else:
        master_list = []

        meet_time_tuples = __generate_meet_time_tuples(a_class)

        for meet_time_tuple in meet_time_tuples:
            if __is_exclusion_meet_time(meet_time_tuple):
                meet_time_tuples.remove(meet_time_tuple)

        master_list += [__row_event(a_class, meet_time[0], meet_time[1]) for meet_time in meet_time_tuples]

    return master_list


def __generate_meet_time_tuples(a_class):
    """
    :param a_class:
    AClass -> class object from a TermSchedule's classes which does not show biweekly behaviour
    :return:
    list -> of tuples (matching the AClass meet time tuple format) of each class day in the semester time start and end
    """
    shift_list = []

    for original_meet_time in a_class.class_time:
        shift_list.append((original_meet_time[0], original_meet_time[1]))  # append first original meet time tuple

        loop_continue = True

        # shift count is used to prevent infinite loop
        max_shift_count = 3 * 4 * 4  # 3 days per 4 weeks for 4 months (assumed max 3 meet times per week)
        shift_count = 0

        while loop_continue and shift_count <= max_shift_count:
            # Get last datetime element in list to shift, and shift by 1 week
            start_shift = shift_list[-1][0] + timedelta(days=7)
            end_shift = shift_list[-1][1] + timedelta(days=7)

            shift_count += 1  # increase shift count

            if SEMESTER_START < start_shift < end_shift < SEMESTER_END:  # ensure all shifts within semester start/end
                shift_list.append((start_shift, end_shift))  # add new meet time tuple to the list
            else:  # if the shift is out of semester scale, end loop
                loop_continue = False

    return shift_list


def __is_exclusion_meet_time(meet_time_tuple):
    """
    Check if a meet_time_tuple falls within an excluded meet time frame (constants.py SEMESTER_EXCLUSION_TIMES)
    :param meet_time_tuple:
    tuple -> Meet time (datetime(), datetime())
    :return:
    bool -> True if there is an exclusion, False if not
    """
    for semester_exclusion in SEMESTER_EXCLUSION_TIMES:
        if semester_exclusion[0] < meet_time_tuple[0] < semester_exclusion[1] or \
                semester_exclusion[0] < meet_time_tuple[1] < semester_exclusion[1]:
            # if start or end of meet_time tuple is within the exclusion time frame return True
            return True

    return False  # default is False


def __row_event(a_class, start_datetime, end_datetime):
    """
    :param a_class:
    AClass -> class object from a TermSchedule's classes
    :return:
    list -> of str defining a class object's details
    """
    # Final Field Data List =
    # ["Subject", "Start Date", "Start Time", "End Date", "End Time", "Description", "Location"]
    return [f"{a_class.title} {a_class.class_type} ({a_class.fac}{a_class.uid})",

            datetime.strftime(start_datetime, "%Y-%m-%d"),

            datetime.strftime(start_datetime, "%H:%M:%S"),

            datetime.strftime(end_datetime, "%Y-%m-%d"),

            datetime.strftime(end_datetime, "%H:%M:%S"),

            f"Professor: {' | '.join(a_class.prof) if len(a_class.prof) > 0 else 'N/A'} & "
            f"CRN: {a_class.crn} & "
            f"Section: {a_class.section}",

            f"Campus: {' | '.join(a_class.campus)} & "
            f"Building: {' | '.join(a_class.building)} & "
            f"Room: {' | '.join(a_class.room)}"]
