#!/usr/bin/env python

import mysql.connector

from ClassStructure.CourseClassStructure import AClass, extract_from_json_str
from redacted import SQL_HOST, SQL_USERNAME, SQL_PASSWORD, SQL_DB


# SQL_HOST = STR mariadb/mysql server host ipv4 address
# SQL_USERNAME = STR user with permissions granted
# SQL_PASSWORD = STR user password
# SQL_DB = STR PainMaker data base name on the server


def __server_connection():
    db_connection = None
    try:
        db_connection = mysql.connector.connect(
            host=SQL_HOST,
            user=SQL_USERNAME,
            passwd=SQL_PASSWORD,
            database=SQL_DB
        )
        # print(f'\n\tSuccessfully connected to mysql DB "{SQL_DB}" AS "{SQL_USERNAME}"')  # TEST CODE
    except Exception as err:
        print(f"\n\tError: '{err}'")

    return db_connection


def pull_class(fac, uid, crn=None):
    """
    :param fac:
    STR faculty value, used to find the table
    :param uid:
    STR uid value, used to find records of all classes
    :param crn:
    INT crn value, used to find a single class
    :return:
    Returns a list of AClass objects
    """
    all_classes_list = []

    connection = __server_connection()
    temp_cursor = connection.cursor(buffered=True)

    temp_cursor.execute(f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name='{fac}'")  # check for table

    if temp_cursor.fetchone()[0] == 1:  # fac table exists
        if crn is None:
            temp_cursor.execute(f"SELECT json_data FROM {fac} WHERE uid='{uid}'")
        else:
            temp_cursor.execute(f"SELECT json_data FROM {fac} WHERE crn={crn}")

        json_strings = temp_cursor.fetchall()

        if len(json_strings) != 0:  # Class exists
            for json_str in json_strings:
                # TODO vvv Check this out, json_str is always a tuple with json_data in index 0, rest of tuple is empty
                all_classes_list.append(extract_from_json_str(json_str[0]))

    return all_classes_list
