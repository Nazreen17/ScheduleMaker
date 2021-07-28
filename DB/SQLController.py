import mysql.connector

from ClassStructure.CourseClassStructure import extract_class_from_json_str
from redacted import SQL_HOST, SQL_USERNAME, SQL_PASSWORD, SQL_DB, SQL_CLASS_TABLE  # SEE -> redactedExample.py


def __server_connection_course():
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


def pull_class_via_redacted(fac, uid, class_type=None, crn=None, seats=None):
    """
    :param fac:
    STR faculty value, used to find the table
    :param uid:
    STR uid value, used to find all classes matching the general course uid
    :param class_type:
    STR class_type value, used to find a instances of a specific class type (Lecture, Tutorial, Laboratory)
    :param crn:
    INT crn value, used to find a single class by crn
    :param seats:
    INT seats value, used to set the minimum seats required
    :return:
    Returns a list of AClass objects
    """
    all_classes_list = []

    connection = __server_connection_course()
    temp_cursor = connection.cursor(buffered=True)
    """
    https://stackoverflow.com/questions/29772337/python-mysql-connector-unread-result-found-when-using-fetchone
    The reason is that without a buffered cursor, the results are "lazily" loaded, meaning that "fetchone" 
    actually only fetches one row from the full result set of the query. When you will use the same cursor again, 
    it will complain that you still have n-1 results (where n is the result set amount) waiting to be fetched. 
    However, when you use a buffered cursor the connector fetches ALL rows behind the scenes and you just take one 
    from the connector so the mysql db won't complain. 
    """

    temp_cursor.execute(f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name='{SQL_CLASS_TABLE}'")
    # check that a table matching fac_str exists

    if temp_cursor.fetchone()[0] == 1:  # fac table exists
        query = f"SELECT json_data FROM {SQL_CLASS_TABLE} WHERE fac='{fac}' AND uid='{uid}'"
        query += f" AND crn={crn}" if crn is not None else ""
        query += f" AND class_type='{class_type}'" if class_type is not None else ""
        query += f" AND seats >= {seats}" if seats is not None else ""

        temp_cursor.execute(query)

        json_strings = temp_cursor.fetchall()

        if len(json_strings) != 0:  # Class exists
            for json_str in json_strings:
                # TODO vvv Check this out, json_str is always a tuple with json_data in index 0, rest of tuple is empty
                all_classes_list.append(extract_class_from_json_str(json_str[0]))
    temp_cursor.close()

    return all_classes_list
