"""
https://www.youtube.com/watch?v=Xjv1sY630Uc
https://selenium-python.readthedocs.io/index.html
https://sites.google.com/a/chromium.org/chromedriver/downloads
"""

import time as no_bork  # as no_bork because "time" may also be used in datetime (datetime is more important so...)
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
#!/usr/bin/env python

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from constants import OTU_COURSE_WEBSITE, CHROMEDRIVER_PATH, TERM, TERM_ID, WEEKDAYS, SLEEP_GENERAL, SLEEP_NEXT_CLASS, \
    SLEEP_TEXT_INPUT, SLEEP_DETAIL_POPUP_TAB, SLEEP_DETAIL_POPUP_TAB_TEXT
from ClassStructure.CourseClassStructure import AClass


def scrape_course_class_objs(course_obj):
    """
    :param course_obj:
    :return:
    return a list of Lecture and Secondary objects
    """

    try:
        driver = webdriver.Chrome(CHROMEDRIVER_PATH)
    except NameError:
        raise NameError("Chromedriver PATH not found")

    class_list = []
    fac = course_obj.fac
    uid = course_obj.uid

    driver.get(OTU_COURSE_WEBSITE)  # open website

    # term input
    driver.find_element_by_id("s2id_txt_term").click()
    term_search = driver.find_element_by_id("s2id_autogen1_search")
    term_search.send_keys(TERM)
    no_bork.sleep(SLEEP_TEXT_INPUT)
    term_search.send_keys(Keys.ENTER)
    driver.find_element_by_id("term-go").click()

    # course num input
    try:  # wait for course num input box to show
        course_num_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "s2id_autogen2")))
        course_num_input.send_keys(str(fac) + str(uid))
        no_bork.sleep(SLEEP_TEXT_INPUT)
        course_num_input.send_keys(Keys.ENTER)
        driver.find_element_by_id("search-go").click()
    except:
        driver.quit()
        raise RuntimeError(str(fac) + str(uid), "does not exist!")

    no_bork.sleep(SLEEP_GENERAL)  # load search

    # class creation
    page_count = 0
    while True:
        page_count += 1
        no_bork.sleep(SLEEP_GENERAL)  # page load
        row_count = len(driver.find_elements_by_xpath('//*[@id="table1"]/tbody/tr'))
        for row in range(1, 1 + row_count):  # range(1, 1 + row_count)
            no_bork.sleep(SLEEP_NEXT_CLASS)
            """
            print("\tReading", str(course_obj.fac).upper(), str(course_obj.uid).upper(), "-> Page #" + str(page_count) +
                  ", Class #" + str(row + (page_count * 10) - 10))
            # progress test print
            """
            class_list.append(__create_class_obj(driver, fac, uid, row))
            if row >= row_count:
                no_bork.sleep(SLEEP_NEXT_CLASS)  # wait to check for next page button
                next_page_button = driver.find_element_by_xpath('//*[@id="searchResultsTable"]/div[2]/div/button[3]')
                check = next_page_button.get_attribute("disabled")
                if check != "true":  # is is not the last page of classes
                    next_page_button.click()  # click to next page
                else:  # this is the last page of classes
                    driver.quit()
                    return class_list


def __create_class_obj(driver, fac, uid, row):
    """
    :param driver:
    :param fac:
    :param uid:
    :return:
    Lecture/Secondary object
    """

    """
    open detailed class info popup
    """
    try:  # wait for table class detailed info popup hyperlink to show
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                        '//*[@id="table1"]/tbody/tr[1]/td[3]/a')))
        driver.find_element_by_xpath('//*[@id="table1"]/tbody/tr[' + str(row) + ']/td[3]/a').click()  # open popup
    except:
        driver.quit()
        raise RuntimeError
    try:  # wait class detailed info to show
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "classDetailsContentDiv")))
    except:
        driver.quit()
        raise RuntimeError

    no_bork.sleep(SLEEP_DETAIL_POPUP_TAB_TEXT)
    detailed_data = str(driver.find_element_by_id("classDetailsContentDiv").text)  # pull str detailed data from popup
    """
    detailed_data example: ...
    Associated Term: Fall 2021\n
    CRN: 43343\n
    Campus: OT-North Oshawa\n
    Schedule Type: Laboratory\n
    Instructional Method: In-class with Streaming Option\n
    Section Number: 007\n
    Subject: Engineering\n
    Course Number: 1015U\n
    Title: Intro. to Engineering\n
    Credit Hours: 3\n
    Grade Mode: Normal Grading Mode (Alpha)
    """

    class_obj = AClass(fac=fac, uid=uid)

    class_obj.crn = __extract_key_data(detailed_data, "CRN: ")
    class_obj.class_type = __extract_key_data(detailed_data, "Schedule Type: ")
    class_obj.title = __extract_key_data(detailed_data, "Title: ")
    class_obj.instruction = __extract_key_data(detailed_data, "Instructional Method: ")
    class_obj.section = __extract_key_data(detailed_data, "Section Number: ")

    seats_and_capacity = __get_seats_and_capacity(driver)
    class_obj.seats = seats_and_capacity[0]
    class_obj.capacity = seats_and_capacity[1]

    # DO NOT SWITCH RIGHT AND LEFT SIDE DATA PULLING (VERY SENSITIVE TO ORDER) vvv
    class_obj.prof = __get_prof_and_expand(driver)  # open class time tab

    no_bork.sleep(SLEEP_DETAIL_POPUP_TAB_TEXT)
    # class time tab: right side
    data_right_side = driver.find_element_by_xpath(
        '//*[@id="classDetailsContentDetailsDiv"]/div/div[2]/div/div[2]').text
    """
    data_right_side example: ...
    08:10 AM - 11:00 AM\n
    OT-North Oshawa Campus | OPG Engineering Building | Room ENG2045
    """
    class_obj.campus = __extract_key_data(data_right_side, "\n", " |")
    class_obj.building = __extract_key_data(data_right_side, "| ", " | Room")
    class_obj.room = __extract_key_data(data_right_side, "Room ")

    # class time tab: left side
    class_obj.class_time = __get_class_time(driver, class_obj.crn)
    class_obj.links = __get_links_list(driver)
    # DO NOT SWITCH RIGHT AND LEFT SIDE DATA PULLING (VERY SENSITIVE TO ORDER) ^^^

    no_bork.sleep(SLEEP_GENERAL)  # wait for button
    # close detailed data popup
    driver.find_element_by_xpath('//button[@class="primary-button small-button"]').click()  # tag=button, @attribute
    # '<button type="button" class="primary-button small-button">Close</button>' # xpath for above ^

    return class_obj


def __get_prof_and_expand(driver):
    no_bork.sleep(SLEEP_DETAIL_POPUP_TAB)
    driver.find_element_by_id("facultyMeetingTimes").click()  # open class meet times

    no_bork.sleep(SLEEP_DETAIL_POPUP_TAB_TEXT)
    collapsed_meet_clicks_count = len(driver.find_elements_by_xpath('//*[@id="classDetailsContentDetailsDiv"]/div/div'))

    if collapsed_meet_clicks_count > 2:  # first "Instructor:Instructor not available" is open by default
        for click_row in range(3, collapsed_meet_clicks_count + 1, 2):  # increment 2
            driver.find_element_by_xpath(
                '//*[@id="classDetailsContentDetailsDiv"]/div/div[' + str(click_row) + ']/span/label').click()
    try:
        return driver.find_element_by_xpath('//*[@id="classDetailsContentDetailsDiv"]/div/div[3]/span/span[1]/a').text
        # assume the first prof is the head prof for all meet times
    except NoSuchElementException:
        return "Unknown"


def __get_seats_and_capacity(driver):
    no_bork.sleep(SLEEP_DETAIL_POPUP_TAB)
    driver.find_element_by_id("enrollmentInfo").click()

    no_bork.sleep(SLEEP_DETAIL_POPUP_TAB_TEXT)
    seat_data = driver.find_element_by_id("classDetailsContentDetailsDiv").text
    """
    seat_data example: ...
    Enrollment Actual: 78\n
    Enrollment Maximum: 130
    """
    seats_taken = int(__extract_key_data(seat_data, "Enrollment Actual: "))
    capacity = int(__extract_key_data(seat_data, "Enrollment Maximum: "))
    return (capacity - seats_taken), capacity


def __get_class_time(driver, crn):
    """
    :param driver:
    :return:
    a list of datetime objects
    """
    datetime_list = []
    meet_time_days = driver.find_elements_by_xpath('//*[@id="' + TERM_ID + '.' + str(crn) + 'div"]')
    for meet_time_indexer in range(len(meet_time_days) // 2):
        collapsed_table_index = (meet_time_indexer + 1) * 2

        # no_bork.sleep(SLEEP_DETAIL_POPUP_TAB_TEXT)  # don't need?
        date_data = driver.find_element_by_xpath('//*[@id="classDetailsContentDetailsDiv"]/div/div[' + str(
            collapsed_table_index) + ']/div/div[1]/div[2]').text  # date data

        day = __extract_key_data(str(meet_time_days[meet_time_indexer].get_attribute("title")), "Class on: ")
        # day is now "Monday", "Tuesday", etc

        # no_bork.sleep(SLEEP_DETAIL_POPUP_TAB_TEXT)  # don't need?
        time_data = driver.find_element_by_xpath('//*[@id="classDetailsContentDetailsDiv"]/div/div[' + str(
            collapsed_table_index) + ']/div/div[2]').text  # time data
        attempt_datetime = __extract_to_datetime(time_data, date_data, day)

        if attempt_datetime is not None:  # rare cases of classes not having any set meet days, ie: COMM1050U >:(
            datetime_list.append(attempt_datetime)

    return datetime_list


def __extract_to_datetime(time_data, datetime_date_obj, day):
    """
    time_date raw data example:
    "02:10 PM - 03:30 PM\n
    OT-Online Campus | Synchronous | Room SYN"
    date_data raw data example:
    "09/07/2021 - 12/06/2021"
    day data example:
    "Monday"
    :param time_data:
    :param datetime_date_obj:
    :param day
    :return:
    [datetime object -> week start + start time, time object -> end time]
    """
    datetime_date_obj = datetime_date_obj[:datetime_date_obj.index("-")].replace(" ", "")
    datetime_date_obj = datetime.strptime(datetime_date_obj, '%m/%d/%Y')

    try:
        target_weekday = WEEKDAYS.index(day)
    except ValueError:  # rare cases of classes not having any set meet days, ie: COMM1050U >:(
        return None

    datetime_date_obj = __next_weekday(datetime_date_obj, target_weekday)

    time_data = time_data.replace(" ", "")
    start = __get_hour_min(time_data[:(time_data.index("-"))])
    end = __get_hour_min(time_data[(time_data.index("-") + 1):])

    elem1 = datetime(datetime_date_obj.year, datetime_date_obj.month, datetime_date_obj.day, start[0], start[1])
    elem2 = datetime(datetime_date_obj.year, datetime_date_obj.month, datetime_date_obj.day, end[0], end[1])

    return elem1, elem2


def __next_weekday(current_datetime_obj, target_weekday_int):
    """
    :param current_datetime_obj:
    :param target_weekday_int:
    0 = Monday, 1 = Tuesday, 2 = Wednesday, etc
    :return:
    datetime object with an adjusted weekday date
    example: target_weekday_int = 6 Saturday -> return the next Saturday as a datetime obj, if the target weekday is
        the current weekday, return result will show the "today" date as it matches the target weekday
    """
    import datetime

    shift = datetime.timedelta((7 + target_weekday_int - current_datetime_obj.weekday()) % 7)
    return current_datetime_obj + shift


def __get_hour_min(time_str):
    """
    :param time_str:
    :return:
    list [hours -> int, minutes -> int]
    """
    hours = int(time_str[:time_str.index(":")])
    minutes = int(time_str[time_str.index(":") + 1:time_str.index(":") + 3])

    hours = hours + 12 if "PM" in time_str and hours != 12 else hours  # change to 24 hour

    return [hours, minutes]


def __get_links_list(driver):
    """
    :param driver:
    :return:
    return LinkOption objects
    """
    # no_bork.sleep(SLEEP_DETAIL_POPUP_TAB)  # don't need?
    driver.find_element_by_id("linked").click()  # open class times

    no_bork.sleep(SLEEP_GENERAL)  # rip some classes have 144 options PAIN the load time

    try:  # wait for all options to load
        num_of_options = len(WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[@id="classDetailsContentDetailsDiv"]/table/tbody'))))
    except:
        driver.quit()
        raise RuntimeError

    combined_options = []
    for option_index in range(1, num_of_options + 1):  # loop through options (Starts at 1 increments by 1)
        links_in_option = []
        num_of_links = len(driver.find_elements_by_xpath(
            '//*[@id="classDetailsContentDetailsDiv"]/table/tbody[' + str(option_index) + ']/tr'))
        for link_index in range(1, num_of_links + 1):
            link_crn = driver.find_element_by_xpath(
                '//*[@id="classDetailsContentDetailsDiv"]/table/tbody[ ' + str(option_index) + ']/tr[' + str(
                    link_index) + ']/td[4]').text
            """
            # once had a possible error solved by this... Not sure if error still happens???
            if len(links_in_option) > 0 and link_crn == links_in_option[-1]:  # prevent recursive element pulling
                raise NoSuchElementException
            """
            links_in_option.append(int(link_crn))
        combined_options.append(links_in_option)

    return combined_options


def __extract_key_data(data, start_key, end_key=None):
    """
    start_key="KEY1", end_key=None
    case A raw data example: "KEY1yoink\n" -> return "yoink"
    case B raw data example: "KEY1 yeet and yoink" -> return "yeet and yoink"
    case C return None
    start_key="KEY1", end_key="KEY2"
    case D raw data example: "KEY1yoinkKEY2\n" -> return "yoink"
    case C return None
    :param data:
    :param start_key:
    :param end_key
    :return:
    """
    extract_data = ""
    if end_key is None:
        try:  # case A (till next line break)
            extract_data = data[(data.index(start_key) + len(start_key)):(data.index("\n", data.index(start_key)))]
        except ValueError:  # case B (all after key)
            try:
                extract_data = data[(data.index(start_key) + len(start_key)):]
            except ValueError:  # case C (None)
                return None
    elif end_key is not None:
        try:  # case C (till next line break)
            extract_data = data[(data.index(start_key) + len(start_key)):(data.index(end_key))]
        except ValueError:  # case E (None)
            return None
    return str(extract_data)
