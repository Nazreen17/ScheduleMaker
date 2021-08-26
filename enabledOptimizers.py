from Optimizations.DayOff import DayOff
from Optimizations.EarlyEnd import EarlyEnd
from Optimizations.InPerson import InPerson
from Optimizations.InPersonNot import Online
from Optimizations.OpenSeats import OpenSeats

ENABLED_OPTIMIZER_OBJECT_LIST = [EarlyEnd(), DayOff(), InPerson(), Online(), OpenSeats()]
# ^^^ ALSO UPDATE: FullProcess/OptimizerRequestStructure.py -> OptimizerRequest.build_request()
