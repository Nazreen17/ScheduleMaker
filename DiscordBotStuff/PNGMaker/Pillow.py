from PIL import Image, ImageDraw, ImageFont

from COREClassStructure.TermScheduleStructure import TermSchedule
from constants import CLASS_INSTRUCTION_IN_PERSON_KEYS, RGB_ONLINE_BLUE, RGB_IN_PERSON_PEACH, SCHEDULE_PNG_FILENAME

COLUMN_SIZE = 200
ROW_SIZE = 80
HEADER_FONT = ImageFont.truetype("DiscordBotStuff/PNGMaker/roboto-mono/RobotoMono-Bold.ttf", 32)
BODY_FONT = ImageFont.truetype("DiscordBotStuff/PNGMaker/roboto-mono/RobotoMono-Medium.ttf", 20)
WEEKDAYS = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]


def draw_png_schedule(schedule_obj):
    """
    draws a .png image of a TermSchedule object
    :param schedule_obj:
    """
    global COLUMN_SIZE, ROW_SIZE, HEADER_FONT, WEEKDAYS

    if not isinstance(schedule_obj, TermSchedule):
        raise TypeError(schedule_obj)

    img = Image.new("RGB", (COLUMN_SIZE * 8, ROW_SIZE * 14), color="white")
    d = ImageDraw.Draw(img)

    for col_i in range(1, 8):
        text = WEEKDAYS[col_i - 1]
        d.text((COLUMN_SIZE * col_i, 10), text, font=HEADER_FONT, fill="black", align="left")

    for row_i in range(8, 21):
        text = str(row_i) + ":00"
        text = " " + text if len(text) < 5 else text
        d.text((10, ROW_SIZE * (row_i - 7)), text, font=HEADER_FONT, fill="black", align="left")
        # time off set >>>>>>>>>>>>>>>>>^ start at 8:00

    if TermSchedule.is_time_valid:
        for class_obj in schedule_obj.classes:
            colour = __get_block_colour_from_instruction_type_str(class_obj.instruction)
            __draw_class(img=img, class_obj=class_obj, block_colour=colour)

    img.save(f"DiscordBotStuff/PNGMaker/{SCHEDULE_PNG_FILENAME}")


def __get_block_colour_from_instruction_type_str(instruction):
    instruction = instruction.lower()

    for key in CLASS_INSTRUCTION_IN_PERSON_KEYS:
        if key.lower() in instruction.lower():  # If the class is in person
            return RGB_IN_PERSON_PEACH
    return RGB_ONLINE_BLUE  # No match, assume online


def __draw_class(img, class_obj, block_colour):
    global COLUMN_SIZE, ROW_SIZE, BODY_FONT

    d = ImageDraw.Draw(img)

    if class_obj.class_time is None:
        return

    for class_time in class_obj.class_time:
        if class_time is not None:
            x_1_cord = COLUMN_SIZE * (class_time[0].weekday() + 2)  # shift weekday indexes (sunday=0) + legend col
            x_2_cord = COLUMN_SIZE * (class_time[0].weekday() + 3)
            y_1_cord = (((class_time[0].hour - 8) + class_time[0].minute / 60) + 1) * ROW_SIZE
            y_2_cord = (((class_time[1].hour - 8) + class_time[1].minute / 60) + 1) * ROW_SIZE

            outline_colour = "black" if class_obj.seats > 0 else "red"

            d.rectangle((x_1_cord, y_1_cord, x_2_cord, y_2_cord), fill=block_colour, outline=outline_colour, width=3)

            text = str(class_obj.fac)[:7] + " " + str(class_obj.uid)[:7]
            d.text((x_1_cord + 10, y_1_cord + 5), text, font=BODY_FONT, fill="black")
            text = str(class_obj.crn)[:15]
            d.text((x_1_cord + 10, y_1_cord + 5 + BODY_FONT.size), text, font=BODY_FONT, fill="black")
            text = str(class_obj.title)[:15 - 4] + " " + str(class_obj.class_type)[:3]
            d.text((x_1_cord + 10, y_1_cord + 5 + (BODY_FONT.size * 2)), text, font=BODY_FONT, fill="black")
