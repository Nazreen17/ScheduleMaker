from Optimizations.DayOff import DayOff
from Optimizations.EarlyEnd import EarlyEnd
from Optimizations.InPerson import InPerson
from Optimizations.InPersonNot import Online

ENABLED_OPTIMIZER_OBJECT_LIST = [EarlyEnd(), DayOff(), InPerson(), Online()]
# ^^^ ALSO UPDATE: FullProcess/OptimizerRequestStructure.py -> OptimizerRequest.build_request()
