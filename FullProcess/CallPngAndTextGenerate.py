from constants import RESULT_TXT_FILENAME
from CacheFilePathManipulation import get_cache_path
from DiscordBotStuff.PNGMaker.Pillow import draw_png_schedule


def generate_png_and_txt(single_term_schedule, result_txt_header_str=None, user_id=None):
    # Generate schedule.png
    draw_png_schedule(single_term_schedule, user_id)

    header = f"{result_txt_header_str}\n------------------------------\n" if result_txt_header_str is not None else ""

    # Generate results.txt
    with open(get_cache_path(RESULT_TXT_FILENAME, user_id), "w") as file:
        file.write(header + single_term_schedule.get_raw_str())
