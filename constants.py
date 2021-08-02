from Optimizations.DayOff import DayOff
from Optimizations.EarlyEnd import EarlyEnd
from Optimizations.InPerson import InPerson
from Optimizations.InPersonNot import Online


MAX_SCHEDULE_COMBINATIONS = 100000

ENABLED_OPTIMIZER_OBJECT_LIST = [EarlyEnd(), DayOff(), InPerson(), Online()]
# ALSO UPDATE: FullProcess/CallOptimizers.py -> __initialize_optimizer()
