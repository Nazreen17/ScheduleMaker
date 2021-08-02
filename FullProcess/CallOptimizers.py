from COREDB.ClassPull import pull_class_object_list_via
from COREDB.MaxTemplatePrivatePull import pull_private_max_schedule_crn_2d_list
from COREDB.MaxTemplatePublicPull import pull_public_max_schedule_crn_2d_list
from constants import ENABLED_OPTIMIZER_OBJECT_LIST

from Optimizations.DayOff import DayOff
from Optimizations.EarlyEnd import EarlyEnd
from Optimizations.InPerson import InPerson
from Optimizations.InPersonNot import Online


def __initialize_optimizer(max_schedules, optimizer_name, optimizer_values=None):
    # ALSO UPDATE: constants.py -> ENABLED_OPTIMIZER_OBJECT_LIST
    optimizer_name.lower().replace(" ", "")

    if optimizer_name == EarlyEnd().name.lower():
        return EarlyEnd(schedule_list=max_schedules)
    elif optimizer_name == DayOff().name.lower():
        return DayOff(schedule_list=max_schedules, day_off=optimizer_values[0])
    elif optimizer_name == InPerson().name.lower():
        return InPerson(schedule_list=max_schedules)
    elif optimizer_name == Online().name.lower():
        return Online(schedule_list=max_schedules)


def get_optimizer(template_id, optimizer_name, user_discord_id, optimizer_values):
    if not __is_valid_optimizer(optimizer_name):  # Ensure that the given optimizer is even valid
        raise ValueError

    # Pull 2D crn code based max schedule list to process
    if template_id == "personal":  # User requests to use personal template
        max_schedules = pull_private_max_schedule_crn_2d_list(user_discord_id)
    else:  # User requests to use public template
        max_schedules = pull_public_max_schedule_crn_2d_list(template_id)

    # Pull all classes based on matching CRN codes
    all_classes = []
    found_crn_classes = []

    for schedule in max_schedules:
        for crn in schedule:
            if crn not in found_crn_classes:
                # Store the first instance of each crn and its AClass value from pulled (indexes match)
                found_crn_classes.append(crn)
                all_classes += pull_class_object_list_via(crn=crn)

    # Convert/Rewrite 2D crn code based max schedule list to 2D AClass based
    for schedule_i in range(len(max_schedules)):
        for crn_i in range(len(max_schedules[schedule_i])):
            max_schedules[schedule_i][crn_i] = all_classes[found_crn_classes.index(max_schedules[schedule_i][crn_i])]
            # Rewrite the 2D max schedule list from crn code based into AClass based

    return __initialize_optimizer(max_schedules, optimizer_name, optimizer_values)


def __is_valid_optimizer(optimizer_name):
    for optimizer in ENABLED_OPTIMIZER_OBJECT_LIST:
        if optimizer_name.lower().replace(" ", "") == optimizer.name.lower().replace(" ", ""):
            return True

    return False
