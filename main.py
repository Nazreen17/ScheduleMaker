# MODULE IS ONLY FOR DEV TESTING ON A LOCAL MACHINE

import time

from enabledOptimizers import ENABLED_OPTIMIZER_OBJECT_LIST
from FullProcess.GeneralProcessing import get_clean_courses_list, generate_png_and_txt
from FullProcess.CallMaxTemplateGeneration import generate_and_update_db_private_template, \
    generate_and_update_db_public_template
from FullProcess.CallOptimizers import request_optimizer
from FullProcess.GeneralProcessing import make_term_schedule_from_crn_no_overhead
from FullProcess.CallCourseRequester import add_course_requests_via_list, drop_course_requests_via_list

# TEST
from MaxSchedule.MaxScheduleGeneration import generate
import json


def test_user_course_request(course_inputs):
    course_object_list = get_clean_courses_list("".join(course_inputs))

    try:
        add_course_requests_via_list(courses_list=course_object_list)
        print(f"Successfully submitted course update request(s)")
    except Exception as e:
        raise e


def test_drop_course_request(course_inputs):
    course_object_list = get_clean_courses_list("".join(course_inputs))

    try:
        drop_course_requests_via_list(courses_list=course_object_list)
        print(f"Successfully removed course update request(s)")
    except Exception as e:
        raise e


def test_generate_private_max_template(course_inputs):
    course_object_list = get_clean_courses_list("".join(course_inputs))

    try:
        generate_and_update_db_private_template(course_object_list=course_object_list,
                                                discord_user_id=None)
        print(f"Successfully generated your personal template")
    except Exception as e:
        raise e


def test_generate_public_max_template(description, course_inputs):
    course_object_list = get_clean_courses_list("".join(course_inputs))

    try:
        generate_and_update_db_public_template(course_object_list=course_object_list, description=description)
        print(f"Successfully generated public template")
    except Exception as e:
        raise e


def test_view_public_templates(public_template_id=None):
    pass


def test_view_private_templates(user_id=None):
    pass


def test_show_all_optimizers():
    optimizer_text = ""
    for optimizer in ENABLED_OPTIMIZER_OBJECT_LIST:
        optimizer_text += f"\nName: **{optimizer.name}**\nDescription: {optimizer.description}"
        if ENABLED_OPTIMIZER_OBJECT_LIST.index(optimizer) != len(ENABLED_OPTIMIZER_OBJECT_LIST) - 1:
            optimizer_text += "\n"

    print(f"**Optimizers ({len(ENABLED_OPTIMIZER_OBJECT_LIST)})**\n{optimizer_text}")


def test_optimize_max(template_id, request_list):
    # Complete command: $ <PublicTemplateId / 'personal'> "<SINGLE_REQUEST#1>" "<SINGLE_REQUEST#1>"
    # <SINGLE_REQUEST#1> format: <OptimizerName>, <ExtraValue#n>, <ExtraValue#n+1>
    request_optimizer(template_id, request_list=request_list)


def test_display_from_crn(crn_codes):
    single_term_schedule = make_term_schedule_from_crn_no_overhead(crn_list=crn_codes)

    result_txt = f"Display Source CRNs =\n{crn_codes}\n"

    generate_png_and_txt(single_term_schedule=single_term_schedule, result_txt_header_str=result_txt)


start = time.time()

# test_optimize_max("3", ["inperson", "dayoff, friday"])
# test_generate_public_max_template("Daniel", ["Math1010u", "math1850u", "engr1015u", "comm1050u", "phy1010u"])

max_schedules = generate(get_clean_courses_list("".join(["engr1015u"])))

with open("yeet1.json", "w") as write_file:
    json.dump(max_schedules, write_file, indent=4)

print(f"Completed in {round(time.time() - start, 2)} sec")
