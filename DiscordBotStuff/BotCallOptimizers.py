from COREDB.ClassPull import pull_class_via_redacted
from Optimizations.DayOff import DayOff
from Optimizations.EarlyEnd import EarlyEnd


def __initialize_optimizer(max_schedules, optimizer_name, optimizer_values=None):
    optimizer_name.lower().replace(" ", "")

    if optimizer_name == EarlyEnd().name.lower().replace(" ", ""):
        return EarlyEnd(schedule_list=max_schedules)
    elif optimizer_name == DayOff().name.lower().replace(" ", ""):
        return DayOff(schedule_list=max_schedules, day_off=optimizer_values[0])


def get_optimized_term_schedule(max_schedules, optimizer_name, optimizer_values=None):
    all_classes = []
    found_crn_classes = []

    for schedule in max_schedules:
        for crn in schedule:
            if crn not in found_crn_classes:
                found_crn_classes.append(crn)
                all_classes += pull_class_via_redacted(crn=crn)
    # Store the first instance of each crn and its AClass value from pulled

    for schedule_i in range(len(max_schedules)):
        for crn_i in range(len(max_schedules[schedule_i])):
            max_schedules[schedule_i][crn_i] = all_classes[found_crn_classes.index(max_schedules[schedule_i][crn_i])]

    if optimizer_values is None:
        optimizer = __initialize_optimizer(max_schedules, optimizer_name)
    else:
        optimizer = __initialize_optimizer(max_schedules, optimizer_name, optimizer_values)

    return optimizer.optimal
