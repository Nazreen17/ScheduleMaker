from Optimizations.DayOff import DayOff
from Optimizations.EarlyEnd import EarlyEnd
from Optimizations.InPerson import InPerson
from Optimizations.InPersonNot import Online


MAX_SCHEDULE_COMBINATIONS = 100000

MAX_OPTIMIZATIONS_PER_REQUEST = 3

MAX_COURSE_UPDATE_REQUESTS = 25

ENABLED_OPTIMIZER_OBJECT_LIST = [EarlyEnd(), DayOff(), InPerson(), Online()]
# ALSO UPDATE: FullProcess/OptimizerRequestStructure.py -> OptimizerRequest.__build_request()
