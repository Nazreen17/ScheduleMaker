"""
Create ics file intended to be used as a calendar, generated from a TermSchedule object.
The calendar will avoid a specified exclusion times set by constants.py
"""

from icalendar import Calendar, Event
from datetime import datetime

from constants import SEMESTER_START, SEMESTER_END, CALENDAR_ICS_FILENAME
from SemesterExclusion.EnabledExclusions import ENABLED_EXCLUSIONS_LIST
from CacheFilePathManipulation import get_cache_path
from COREClassStructure.CourseClassStructure import AClass


def create_calendar_from_term_schedule(term_schedule, user_id=None):
    """
    void -> Create ics file
    :param term_schedule:
    TermSchedule -> to translate to ics calendar
    :param user_id:
    str -> User id, default None
    :return:
    """
    calendar = Calendar()

    events = __build_event_list_from_a_class(term_schedule.classes.copy())
    events += __build_exclusion_event_list()

    for event in events:
        calendar.add_component(event)

    with open(get_cache_path(CALENDAR_ICS_FILENAME, user_id), "wb") as file:
        file.write(calendar.to_ical())


def __build_event_list_from_a_class(a_class_list):
    """
    :param a_class_list:
    list or AClass -> list of AClass or single AClass to turn into an event(s)
    :return:
    list -> of all AClass object(s) translated into icalendar.Event(s)
    """
    # Ensure type instance
    if isinstance(a_class_list, AClass):
        a_class_list = [a_class_list]
    elif not isinstance(a_class_list, list) and not isinstance(a_class_list, tuple):
        raise TypeError(f"Expected list, tuple or AClass type")

    # Compute/create/translate events
    events_list = []

    for a_class in a_class_list:
        if len(a_class.class_time) > 0:  # Ensure at least 1 class meet time tuple
            for meet_time_tuple in a_class.class_time:

                if a_class.is_biweekly_specific():  # biweekly, disable recurrence
                    events_list.append(__build_recurring_events(a_class=a_class, meet_time_tuple=meet_time_tuple,
                                                                biweekly_specific=True))

                else:  # Not biweekly, enable recurrence only should be required on non biweekly specific class
                    events_list.append(__build_recurring_events(a_class=a_class, meet_time_tuple=meet_time_tuple,
                                                                biweekly_specific=False))

    return events_list


def __build_recurring_events(a_class, meet_time_tuple, biweekly_specific=True):
    """
    :param a_class:
    AClass -> to get basic information from
    :param meet_time_tuple:
    tuple -> datetime.datetime standard 2 element meet time tuple, used to set actual event times
    :param biweekly_specific:
    bool -> True for biweekly specific, else False, Default True (True means no recurrence)
    :return:
    icalendar.Event -> translated AClass
    """
    event = Event()

    # Summary setting
    summary = f"{a_class.title} {a_class.class_type} ({a_class.fac}{a_class.uid})"
    event.add("summary", summary)

    # Description setting
    description = (f"Professor: {' | '.join(a_class.prof) if len(a_class.prof) > 0 else 'N/A'}\n"
                   f"CRN: {a_class.crn}\n"
                   f"Section: {a_class.section}\n"
                   f"Campus: {' | '.join(a_class.campus) if len(a_class.campus) > 0 else 'N/A'}\n"
                   f"Building: {' | '.join(a_class.building) if len(a_class.building) > 0 else 'N/A'}\n"
                   f"Room: {' | '.join(a_class.room) if len(a_class.room) > 0 else 'N/A'}")
    event.add("description", description)

    # Location setting
    location = (f"Campus: {' | '.join(a_class.campus)} & Building: {' | '.join(a_class.building)} & "
                f"Room: {' | '.join(a_class.room)}")
    event.add("location", location)

    # Datetime start and end setting
    if SEMESTER_START < meet_time_tuple[0] < SEMESTER_END and SEMESTER_START < meet_time_tuple[1] < SEMESTER_END:
        event.add("dtstart", meet_time_tuple[0])
        event.add("dtend", meet_time_tuple[1])

    # Recurrence/Repeating frequency rule setting
    if not biweekly_specific:
        event.add("rrule", {"FREQ": "WEEKLY", "UNTIL": SEMESTER_END})

    # Datetime stamp setting
    event.add("dtstamp", datetime.now())

    return event


def __build_exclusion_event_list():
    """
    Add all enabled exclusions as events to all schedules
    :return:
    list -> icalendar.Event(s)
    """
    exclusion_event_list = []

    for exclusion in ENABLED_EXCLUSIONS_LIST:
        for exclusion_time_tuple in exclusion.get_exclusion_times():
            event = Event()

            # Summary setting
            event.add("summary", exclusion.get_name())

            # Description setting
            event.add("description", exclusion.get_description())

            event.add("dtstart", exclusion_time_tuple[0])
            event.add("dtend", exclusion_time_tuple[1])

            # Datetime stamp setting
            event.add("dtstamp", datetime.now())

            exclusion_event_list.append(event)

    return exclusion_event_list
