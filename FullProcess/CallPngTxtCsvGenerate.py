from constants import RESULT_TXT_FILENAME
from CacheFilePathManipulation import get_cache_path
from FullProcess.PNGMaker.CallPillow import draw_png_schedule
from FullProcess.ICSManipulation import create_calendar_from_term_schedule


def generate_triple_png_txt_csv(single_term_schedule, result_txt_header_str=None, user_id=None):
    """
    void -> Generate schedule.png, results.txt, calendar.csv
    :param single_term_schedule:
    :param result_txt_header_str:
    :param user_id:
    :return:
    """
    # generate schedule.png
    draw_png_schedule(single_term_schedule, user_id)

    # generate results.txt
    write_results_txt(single_term_schedule, result_txt_header_str, user_id)

    # generate calendar.csv
    create_calendar_from_term_schedule(single_term_schedule, user_id)


def write_results_txt(single_term_schedule, result_txt_header_str=None, user_id=None):
    """
    void -> Create results.txt file
    :param single_term_schedule:
    :param result_txt_header_str:
    :param user_id:
    """
    header = f"{result_txt_header_str}\n------------------------------\n" if result_txt_header_str is not None else ""

    # generate results.txt
    with open(get_cache_path(RESULT_TXT_FILENAME, user_id), "w") as file:
        file.write(header + single_term_schedule.get_raw_str())
