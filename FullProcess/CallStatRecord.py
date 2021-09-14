"""
Check COREDB.StatsUpdate and COREDB.StatsPull for documentation
"""

from COREDB.StatsUpdate import add_new_stat
from COREDB.StatsPull import read_all_stats, get_stat_count


def call_stat_count(*descriptions):
    for description in descriptions:
        if not isinstance(description, str):
            raise TypeError("Expected str")

    return get_stat_count(descriptions)


def call_all_stats(*descriptions):
    for description in descriptions:
        if not isinstance(description, str):
            raise TypeError("Expected str")

    return read_all_stats(descriptions)


def call_add_stat(description):
    if isinstance(description, str):
        add_new_stat(description)
    else:
        raise TypeError("Expected str")
