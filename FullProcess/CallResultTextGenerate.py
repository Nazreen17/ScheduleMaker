def full_result_text(term_schedule, search_crn_codes=None):
    """
    :param term_schedule:
    TermSchedule -> Result TermSchedule
    :param search_crn_codes:
    list -> of initial CRN search crn codes
    :return:
    str -> Result message (Combined with warning_message_text())
    """
    # Generate Result text
    found_crn_codes_str = [str(class_object.crn) for class_object in term_schedule.classes]

    result_txt = (f"Schedule CRNs: {', '.join(found_crn_codes_str)}\n"
                  f"{warning_message_text(term_schedule, search_crn_codes)}")

    return result_txt


def warning_message_text(term_schedule, search_crn_codes=None):
    """
    :param term_schedule:
    TermSchedule -> Result TermSchedule
    :param search_crn_codes:
    list -> of initial CRN search crn codes
    :return:
    str -> Warning message
    """
    warning_message = []

    # Check for possible bad crn codes if search_crn_codes is not None
    if search_crn_codes is not None and len(term_schedule) != len(search_crn_codes):
        found_crn_codes_str = [class_object.crn for class_object in term_schedule.classes]
        # Combine all found crn codes
        warning_message.append(f"WARNING: Could not find {', '.join(set(search_crn_codes) - set(found_crn_codes_str))}.")

    # Check for possible time conflict
    if not term_schedule.is_time_valid():
        warning_message.append("WARNING: Time conflict detected.")

    # Check for link satisfaction
    is_links_satisfied, offender = term_schedule.all_links_satisfied_with_a_class_offender()
    if not is_links_satisfied:
        warning_message.append(f"WARNING: Class links are unsatisfied! First offender: "
                               f"{offender.fac}{offender.uid} ({offender.crn})")

    # Check for open seats
    is_open_seats, offender = term_schedule.all_open_seats_with_a_class_offender()
    if not is_open_seats:
        warning_message.append(f"WARNING: Class(es) may have no seats left! First offender: "
                               f"{offender.fac}{offender.uid} ({offender.crn})\n")

    # Final format
    if len(warning_message) > 0:
        warning_message = "\n".join(warning_message)
        warning_message = f"\n{warning_message}"
    else:
        warning_message = ""

    return warning_message
