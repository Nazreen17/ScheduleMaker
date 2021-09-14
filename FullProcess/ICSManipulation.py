"""
Create ics file intended to be used as a calendar, generated from a TermSchedule object.
The calendar will avoid a specified exclusion times set by constants.py
"""

from icalendar import Calendar, Event
from datetime import datetime

from constants import CALENDAR_ICS_FILENAME
from config import SEMESTER_START, SEMESTER_END, ENABLED_EXCLUSIONS_LIST
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

    events = __build_event_list_from_a_class(term_schedule.classes)
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
            events_list += __build_recurring_events(a_class)

    return events_list


def __build_recurring_events(a_class):
    """
    :param a_class:
    AClass -> to get basic information from
    :return:
    list -> of icalendar.Event(s) of translated AClass
    """
    events_list = []

    if not a_class.is_biweekly_specific() and not a_class.not_biweekly_different_times():  # Not biweekly, and all same
        # class_times. Create 1 event with weekly recurrence

        single_event = __initialize_event(a_class)

        # Datetime start and end setting
        first_start, first_end = __first_start_and_end_after_sem_start(a_class.class_time.copy())
        single_event.add("dtstart", first_start)  # Create first event start and end
        single_event.add("dtend", first_end)

        # Recurrence/Repeating frequency rule setting
        day_dict = {0: "MO", 1: "TU", 2: "WE", 3: "TH", 4: "FR", 5: "SA",
                    6: "SU"}  # Heads up: datetime uses 0=Monday VS icalendar uses 0=Sunday
        days = [day_dict[meet_time[0].weekday()] for meet_time in a_class.class_time]  # List of all days for class
        single_event.add("rrule", {"FREQ": "WEEKLY", "UNTIL": SEMESTER_END, "BYDAY": days})  # Recurrence rule

        events_list.append(single_event)

    else:  # Is biweekly specific or (is not biweekly class times on different days and times). Create multiple events.
        for meet_time in a_class.class_time:
            multi_event = __initialize_event(a_class)

            # Datetime start and end setting
            multi_event.add("dtstart", meet_time[0])  # Create first event start and end
            multi_event.add("dtend", meet_time[1])

            events_list.append(multi_event)

    return events_list


def __initialize_event(a_class):
    """
    :param a_class:
    AClass -> class object to translate to event
    :return:
    icalendar.Event() -> class translated to event
    """
    event = Event()

    # Summary setting
    summary = f"{a_class.title} {a_class.class_type[:3].upper()} ({a_class.fac}{a_class.uid})"
    event.add("summary", summary)

    # Format str data
    if a_class.room is not None and 1 < len(a_class.room) == a_class.room.count(a_class.room[0]):
        # All repeating classes (more than 1) in same room
        campus_str_data = a_class.campus[0]
        building_str_data = a_class.building[0]
        room_str_data = a_class.room[0]
    elif a_class.campus is not None and len(a_class.campus) > 0:
        campus_str_data = ", ".join(a_class.campus)
        building_str_data = ", ".join(a_class.building)
        room_str_data = ", ".join(a_class.room)
    else:
        campus_str_data = "N/A"
        building_str_data = "N/A"
        room_str_data = "N/A"

    # Description setting
    description = (
        f"Instructor: {', '.join(a_class.prof) if a_class.prof is not None and len(a_class.prof) > 0 else 'N/A'}\n"
        f"CRN: {a_class.crn}\n"
        f"Section: {a_class.section}\n"
        f"Campus: {campus_str_data}\n"
        f"Building: {building_str_data}\n"
        f"Room: {room_str_data}")
    event.add("description", description)

    # Location setting
    location = f"Campus: {campus_str_data}, Building: {building_str_data}, Room: {room_str_data}"
    event.add("location", location)

    # Datetime stamp setting
    event.add("dtstamp", datetime.now())

    return event


def __first_start_and_end_after_sem_start(class_times):
    """
    :param class_times:
    AClass -> Get first start and end of a meet time
    :return:
    datetime.datetime, datetime.datetime -> of start and end datetime.datetime of the first meet time after the
    SEMESTER_START datetime
    """
    best = None

    for meet_time_tuple in class_times:
        if SEMESTER_START < meet_time_tuple[0] and (best is None or meet_time_tuple < best):  # (Just use start time
            # for comparisons)
            # meet_time_start is greater/newer than the SEMESTER_START, then... best is not set or the new meet_time is
            # better (More closer be age to the SEMESTER_START)
            best = meet_time_tuple

    return best  # Return best meet_time_tuple (best_start_datetime, best_end_datetime)


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
