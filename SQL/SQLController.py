#!/usr/bin/env python

import mysql.connector

from ClassStructure.CourseClassStructure import AClass
from redacted import SQL_HOST, SQL_USER, SQL_PASS


def server_connection(host_name, user_name, user_password):
    db_connection = None
    try:
        db_connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Exception as err:
        print(f"Error: '{err}'")

    return db_connection


def check_add_faculty(fac):
    temp_cursor = server_connection(host_name=SQL_HOST, user_name=SQL_USER, user_password=SQL_PASS).cursor()

    if __table_exists(fac):
        temp_cursor.execute(
            f"CREATE TABLE '{fac}' (id INT AUTO_INCREMENT PRIMARY KEY, crn INTEGER (10), uid VARCHAR(10), "
            "seats INTEGER (5), class_type VARCHAR(10), json_data VARCHAR(2500))")

    temp_cursor.close()
    return False


def __table_exists(table_name):
    temp_cursor = server_connection(host_name=SQL_HOST, user_name=SQL_USER, user_password=SQL_PASS).cursor()

    temp_cursor.execute(f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{table_name}'")
    if temp_cursor.fetchone()[0] == 1:
        temp_cursor.close()
        return True

    temp_cursor.close()
    return False


def update_class(class_obj):
    if not isinstance(class_obj, AClass):
        return
    if not __table_exists(class_obj.fac):
        check_add_faculty(class_obj.fac)

    temp_cursor = server_connection(host_name=SQL_HOST, user_name=SQL_USER, user_password=SQL_PASS).cursor()

    temp_cursor.execute(f"SELECT EXISTS(SELECT 1 FROM '{class_obj.fac}' WHERE crn = '{class_obj.crn}')")
    # Select an existing row with matching crn

    # TODO Still need to finish logic, saving for backup sake. Check if class row exists, add or update as needed

    temp_cursor.execute(f"INSERT INTO '{class_obj.fac}' (crn, uid, seats, class_type, json_data) "
                        "VALUES (class_obj.crn, class_boj.uid, class_obj.seats, class_obj.class_type, ext_data)")

    temp_cursor.close()
    return False
