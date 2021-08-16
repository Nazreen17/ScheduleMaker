from DiscordBotStuff.PNGMaker.Pillow import draw_png_schedule


def generate_png_and_txt(single_term_schedule, result_txt_header_str=None):
    # Generate schedule.png
    draw_png_schedule(single_term_schedule)

    header = f"{result_txt_header_str}\n------------------------------\n" if result_txt_header_str is not None else ""

    # Generate results.txt
    with open("DiscordBotStuff/result.txt", "w") as file:
        file.write(header + single_term_schedule.get_raw_str())