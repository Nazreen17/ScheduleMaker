from COREDB.MaxTemplatePrivateUpdate import update_private_max_template
from COREDB.MaxTemplatePublicUpdate import update_public_max_template
from COREDB.MaxTemplatePublicPull import get_public_id_from_private_course_manifest
from FullProcess.MaxScheduleGeneration import generate


def generate_and_update_db_private_template(course_object_list, discord_user_id):
    course_raw_str_list = []
    for course in course_object_list:
        course_raw_str_list.append(course.get_raw_str())

    public_id_num = get_public_id_from_private_course_manifest(course_raw_str_list=course_raw_str_list)

    if public_id_num < 0:  # No public match, save this private custom max schedule template
        max_schedules = generate(course_object_list)

        if len(max_schedules) > 0:
            update_private_max_template(max_schedule=max_schedules, discord_user_id=discord_user_id)
    else:
        raise RuntimeError


def generate_and_update_db_public_template(course_object_list, description=None):
    max_schedules = generate(course_object_list)

    if len(max_schedules) > 0:
        update_public_max_template(max_schedule=max_schedules, description=description)
