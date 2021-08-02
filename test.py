# MODULE IS ONLY FOR DEV TESTING ON A LOCAL MACHINE

from FullProcess.CallOptimizers import get_optimizer
from FullProcess.GeneralProcessing import generate_png_and_txt


def test_optimizer(template_id, optimizer_name, user_discord_id, optimizer_values):
    optimizer = get_optimizer(template_id=template_id, optimizer_name=optimizer_name, user_discord_id=user_discord_id,
                              optimizer_values=optimizer_values)

    single_term_schedule = optimizer.optimal
    result_txt = f"OPTIMIZER.result =\n{optimizer.result}\n"

    generate_png_and_txt(single_term_schedule=single_term_schedule, result_txt_header_str=result_txt)


# test_optimizer(template_id=1, optimizer_name="dayoff", user_discord_id=0, optimizer_values=("fri"))
