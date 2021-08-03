# MODULE IS ONLY FOR DEV TESTING ON A LOCAL MACHINE

from FullProcess.CallOptimizers import request_optimizer


def test_optimizer(template_id, request_list):
    # Complete command: $ <PublicTemplateId / 'personal'> "<SINGLE_REQUEST#1>" "<SINGLE_REQUEST#1>"
    # <SINGLE_REQUEST#1> format: <OptimizerName>, <ExtraValue#n>, <ExtraValue#n+1>
    request_optimizer(template_id, request_list=request_list)


test_optimizer("3", ["inperson", "dayoff, friday"])
