from COREClassStructure.TermScheduleStructure import TermSchedule
from COREDB.ClassPull import pull_class_object_list_via


def generate_term_schedule_from_crn_list(crn_codes_list):
    """
    :param crn_codes_list:
    list -> List of CRN codes
    :return:
    return a
    """
    # Ensure CRN codes specified
    if len(crn_codes_list) == 0:
        raise ValueError("No CRN codes were specified!")

    # Pull all classes via the specified CRN Codes
    class_objects_list = []
    for crn in crn_codes_list:
        class_objects_list += pull_class_object_list_via(crn=crn)

    # Generate a TermSchedule
    single_term_schedule = TermSchedule(class_objects_list)

    # Check for possible bad CRN codes
    if len(single_term_schedule.classes) == 0:
        raise ValueError("None of the CRN codes specified could be found!\n"
                         "Please send a course update request if needed")

    """
    elif len(single_term_schedule.classes) != len(crn_codes_list):  # All classes with matching CRNs were found
        raise RuntimeWarning("Some CRN codes specified could not be found")
    """

    return single_term_schedule
