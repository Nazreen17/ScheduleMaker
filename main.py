from Menu import get_courses_list
from JSONCourses.JSONCoursesManip import update_course_json
from JSONMaxSchedules.ScheduleGeneration import generate
from JSONMaxSchedules.JSONSchedulesManip import save_schedule_json
# from Optimizations.


def main():
    is_invalid_mode = True
    current_mode = ""
    valid_modes = ["update", "generate", "optimize"]

    while is_invalid_mode:
        current_mode = input("MODE > ").lower()
        if current_mode not in valid_modes:
            print("\tERROR: Invalid mode! Valid modes:", valid_modes)
        else:
            is_invalid_mode = False

    if current_mode == valid_modes[0]:  # update DB
        print("\tMODE =", valid_modes[0].upper())
        update_course_json(get_courses_list())
    elif current_mode == valid_modes[1]:  # generate courses
        print("\tMODE =", valid_modes[1].upper())
        all_schedules_list = generate(get_courses_list())
        file_name = input("Enter a filename.json to save schedules to > ")
        save_schedule_json(file_name, all_schedules_list)
    elif current_mode == valid_modes[2]:  # optimize
        print("\tMODE =", valid_modes[2].upper())
        # optimize()


if __name__ == "__main__":
    main()
