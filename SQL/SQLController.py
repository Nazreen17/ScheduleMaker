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
        temp_cursor.execute("CREATE TABLE fac (id INT AUTO_INCREMENT PRIMARY KEY, crn INTEGER (10), uid VARCHAR(10), "
                            "seats INTEGER (5), data VARCHAR(2500))")

    temp_cursor.close()
    return False


def __table_exists(table_name):
    temp_cursor = server_connection(host_name=SQL_HOST, user_name=SQL_USER, user_password=SQL_PASS).cursor()

    temp_cursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(table_name.replace('\'', '\'\'')))
    if temp_cursor.fetchone()[0] == 1:
        temp_cursor.close()
        return True

    temp_cursor.close()
    return False


def update_class(class_obj):
    if isinstance(class_obj, AClass):
        pass
