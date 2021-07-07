from Menu import get_courses_list
from JSONCourses.DBv1CoursesFileManip import update_course_file
from DBv1Schedules.ScheduleGeneration import generate
from DBv1Schedules.DBv1ScheduleFileManip import schedules_write
from DBv1Optimized.ScheduleOptimization import optimize


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
        update_course_file(get_courses_list())
    elif current_mode == valid_modes[1]:  # generate courses
        print("\tMODE =", valid_modes[1].upper())
        courses_list = get_courses_list()
        all_schedules_list = generate(courses_list)
        file_name = input("Enter a filename.txt to save schedules to > ")
        schedules_write(file_name, all_schedules_list, courses_list)
    elif current_mode == valid_modes[2]:  # optimize
        print("\tMODE =", valid_modes[2].upper())
        optimize()


if __name__ == "__main__":
    main()
