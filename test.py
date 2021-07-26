# THIS FILE IS ONLY FOR LOCAL MACHINE TESTING

from DiscordBotStuff.BotExtraProcessing import get_clean_courses_list
from MaxScheduleTemplates.MaxTemplateGeneration import generate


def test():
    # TEST CODE FOR RUNNING MAX_SCHEDULE LOCALLY
    course_inputs = "math1850u engr1015u"

    all_courses_list = get_clean_courses_list(course_inputs)
    max_schedules = generate(all_courses_list)
    print(f"max_schedules: {max_schedules}")


# test()
