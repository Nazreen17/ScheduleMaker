from redacted import SQL_CLASS_TABLE
from ClassStructure.CourseClassStructure import AClass, convert_class_to_json_str
from COREDB.SQLConnection import server_connection


def update_class(class_obj):
    if not isinstance(class_obj, AClass):
        return

    __check_add_class_table_via_redacted()
    __check_add_class_record_via_redacted(class_obj)


def __check_add_class_table_via_redacted():
    connection = server_connection()
    temp_cursor = connection.cursor()

    temp_cursor.execute(f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name='{SQL_CLASS_TABLE}'")

    if temp_cursor.fetchone()[0] != 1:  # fac table does not exist yet, add new fac table
        # ^^^ temp_cursor.fetchone()[0] == 1  # means a table exists
        temp_cursor.execute(f"CREATE TABLE {SQL_CLASS_TABLE} "
                            "(crn INTEGER(10) NOT NULL, fac VARCHAR(10) NOT NULL, uid VARCHAR(10) NOT NULL, "
                            "seats INTEGER(3) NOT NULL DEFAULT 1, class_type VARCHAR(10) NOT NULL, "
                            "json_data JSON NOT NULL, PRIMARY KEY(crn))")
        # WARNING/NOTE: The default seats value is 1 (Assumes all class has 1 seat open if no specified value)
        connection.commit()
    temp_cursor.close()
    connection.close()


def __check_add_class_record_via_redacted(class_obj):
    connection = server_connection()
    temp_cursor = connection.cursor(buffered=True)
    """
    https://stackoverflow.com/questions/29772337/python-mysql-connector-unread-result-found-when-using-fetchone
    The reason is that without a buffered cursor, the results are "lazily" loaded, meaning that "fetchone" 
    actually only fetches one row from the full result set of the query. When you will use the same cursor again, 
    it will complain that you still have n-1 results (where n is the result set amount) waiting to be fetched. 
    However, when you use a buffered cursor the connector fetches ALL rows behind the scenes and you just take one 
    from the connector so the mysql db won't complain. 
    """

    temp_cursor.execute(f"SELECT * FROM {SQL_CLASS_TABLE} WHERE crn={class_obj.crn}")
    # Select an existing row with matching crn

    if temp_cursor.rowcount == 0:  # Class does not exist on a record yet
        temp_cursor.execute(f"INSERT INTO {SQL_CLASS_TABLE} (crn, fac, uid, seats, class_type, json_data) "
                            f"VALUES ({class_obj.crn}, '{class_obj.fac}', '{class_obj.uid}', {class_obj.seats}, "
                            f"'{class_obj.class_type}', '{convert_class_to_json_str(class_obj)}')")
    else:  # class exists, only update seats and json extended data
        temp_cursor.execute(f"UPDATE {SQL_CLASS_TABLE} "
                            f"SET seats={class_obj.seats}, json_data='{convert_class_to_json_str(class_obj)}' "
                            f"WHERE crn={class_obj.crn}")
    connection.commit()
    temp_cursor.close()
    connection.close()
