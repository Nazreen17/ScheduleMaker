import json

from ClassStructure.MaxSchedulesStructure import TermScheduleDecoder
from ClassStructure.CourseStructure import AClassEncoder


def save_schedule_json(file_name, all_schedules_list):
    __write_schedule_objs(file_name, all_schedules_list)
    print("\tUpdated:", file_name + ".json")


def __write_schedule_objs(file_name, all_schedules_list):
    file_name = file_name if file_name[-5:] == ".json" else file_name + ".json"  # ensure .json file type in file_name
    file_name = file_name if file_name[:17] == "JSONMaxSchedules/" else "JSONMaxSchedules/" + file_name
    # ensure proper filepath


    try:
        with open(file_name, "w") as write_file:
            json.dump(all_schedules_list, write_file, indent=4, default=AClassEncoder.default)
    except FileNotFoundError:
        with open(file_name[17:], "w") as write_file:
            json.dump(all_schedules_list, write_file, indent=4, default=AClassEncoder.default)


def extract_schedule_list(file_name):
    return __read_schedule_objs(file_name)


def __read_schedule_objs(file_name):
    file_name = file_name if file_name[-5:] == ".json" else file_name + ".json"  # ensure .json file type in file_name
    file_name = file_name if file_name[:17] == "../JSONMaxSchedules/" else "../JSONMaxSchedules/" + file_name
    # ensure proper filepath

    try:
        with open(file_name, "r") as reading_file:
            class_obj_list = json.load(reading_file, cls=TermScheduleDecoder)
    except FileNotFoundError:
        with open(file_name[17:], "r") as reading_file:
            class_obj_list = json.load(reading_file, cls=TermScheduleDecoder)

    return class_obj_list
