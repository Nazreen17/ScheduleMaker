from COREDB.ClassPull import pull_class_via_redacted
from COREDB.MaxTemplatePrivatePull import pull_private_max_schedule_crn_2d_list
from COREDB.MaxTemplatePublicPull import pull_public_max_schedule_crn_2d_list
from Optimizations.DayOff import DayOff
from Optimizations.EarlyEnd import EarlyEnd
from constants import ENABLED_OPTIMIZER_OBJECT_LIST
from DiscordBotStuff.PNGMaker.Pillow import draw_png_schedule


def run_optimizer(template_id, optimizer_name, author_id, additional_optimizer_values):
    if not __is_valid_optimizer(optimizer_name):
        raise ValueError

    if template_id == "personal":
        max_schedules = pull_private_max_schedule_crn_2d_list(author_id)
    else:
        max_schedules = pull_public_max_schedule_crn_2d_list(template_id)

    completed_optimizer = __get_optimizer(max_schedules=max_schedules, optimizer_name=optimizer_name,
                                          optimizer_values=additional_optimizer_values)

    # Generate schedule.png
    single_term_schedule = completed_optimizer.optimal
    draw_png_schedule(single_term_schedule)

    # Generate results.txt
    results = completed_optimizer.result
    result_txt = f"OPTIMIZER.result =\n{results}\n------------------------------\n"
    with open("DiscordBotStuff/result.txt", "w") as file:
        file.write(result_txt + single_term_schedule.get_raw_str())


def __is_valid_optimizer(optimizer_name):
    for optimizer in ENABLED_OPTIMIZER_OBJECT_LIST:
        if optimizer_name.lower().replace(" ", "") == optimizer.name.lower().replace(" ", ""):
            return True

    return False


def __initialize_optimizer(max_schedules, optimizer_name, optimizer_values=None):
    optimizer_name.lower().replace(" ", "")

    if optimizer_name == EarlyEnd().name.lower().replace(" ", ""):
        return EarlyEnd(schedule_list=max_schedules)
    elif optimizer_name == DayOff().name.lower().replace(" ", ""):
        return DayOff(schedule_list=max_schedules, day_off=optimizer_values[0])


def __get_optimizer(max_schedules, optimizer_name, optimizer_values=None):
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

    return optimizer
