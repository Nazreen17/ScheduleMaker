from constants import MAX_OPTIMIZATIONS_PER_REQUEST
from Optimizations.OptimizerRequestStructure import OptimizerRequest


def get_requested_optimizer(template_id, request_list, user_discord_id=None):
    """
    VOID function, generate new max_schedule
    :param template_id:
    :param request_list:
    :param user_discord_id:
    """
    if len(request_list) > MAX_OPTIMIZATIONS_PER_REQUEST:
        raise RuntimeError(f"Surpassed MAX_OPTIMIZATIONS_PER_REQUEST = {MAX_OPTIMIZATIONS_PER_REQUEST}"
                           f" < {len(request_list)}")

    last_optimizer_obj = None

    for i in range(len(request_list)):
        request_list[i] = request_list[i].replace(" ", "")
        request_list[i] = request_list[i].translate({ord(c): "" for c in "!@#$%^&*()[]{};:./<>?\\|`~-=_+"})
        request_list[i] = request_list[i].split(",")
        for request_field in request_list[i]:
            if request_field == "":
                request_list[i].remove(request_field)

    for i in range(len(request_list)):
        request = OptimizerRequest()
        # Complete command: $ <PublicTemplateId / 'personal'> "<SINGLE_REQUEST#1>" "<SINGLE_REQUEST#1>"
        # <SINGLE_REQUEST#1> format: <OptimizerName>, <ExtraValue#n>, <ExtraValue#n+1>
        request.user_discord_id = user_discord_id
        request.template_id = template_id
        request.optimizer_name = request_list[i][0]
        request.extra_values = request_list[i][1:]

        if i == 0:  # Single request
            request.single_request_build_max_schedule_from_self()

        elif last_optimizer_obj is not None and len(last_optimizer_obj.ties) == 1:  # No more optimization possible
            return last_optimizer_obj

        else:  # Multi request
            request.max_schedule = last_optimizer_obj.ties

        last_optimizer_obj = request.build_request()

    return last_optimizer_obj
