from COREDB.SQLConnection import server_connection
from redacted import SQL_PRIVATE_MAX_TEMPLATE_TABLE
import json


def update_private_max_template(max_schedule, discord_user_id=None):
    __check_add_private_max_template_table()
    __check_add_private_max_template_record(max_schedule=max_schedule, discord_user_id=discord_user_id)


def __check_add_private_max_template_table():
    connection = server_connection()
    temp_cursor = connection.cursor()

    temp_cursor.execute(f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name='"
                        f"{SQL_PRIVATE_MAX_TEMPLATE_TABLE}'")

    if temp_cursor.fetchone()[0] != 1:  # fac table does not exist yet, add new fac table
        # ^^^ temp_cursor.fetchone()[0] == 1  # means a table exists
        temp_cursor.execute(f"CREATE TABLE {SQL_PRIVATE_MAX_TEMPLATE_TABLE} "
                            "(id INT NOT NULL AUTO_INCREMENT, user INTEGER(18) NOT NULL, "
                            "crn_2d_json JSON NOT NULL, PRIMARY KEY(id))")
        connection.commit()
    temp_cursor.close()
    connection.close()


def __check_add_private_max_template_record(max_schedule, discord_user_id):
    """
    Void function, adds a MaxSchedule 2D list to the SQL data base at table_name
    :param max_schedule:
    A 2d list of int CRN codes
    :param discord_user_id:
    18 digit long int from discord's user id format
    :return:
    """
    connection = server_connection()
    temp_cursor = connection.cursor(buffered=True)

    temp_cursor.execute(f"SELECT * FROM {SQL_PRIVATE_MAX_TEMPLATE_TABLE} WHERE user={discord_user_id}")
    # Select an existing row with matching crn

    # 2D list of integers do not need a custom encoder, just use json.dumps()

    if temp_cursor.rowcount == 0:  # Private User's MaxSchedule does not exist on a record yet
        temp_cursor.execute(f"INSERT INTO {SQL_PRIVATE_MAX_TEMPLATE_TABLE} (user, crn_2d_json) "
                            f"VALUES ({discord_user_id}, '{json.dumps(max_schedule)}')")
    else:  # Private Private User's MaxSchedule exists, update/overwrite
        temp_cursor.execute(f"UPDATE {SQL_PRIVATE_MAX_TEMPLATE_TABLE} "
                            f"SET crn_2d_json='{json.dumps(max_schedule)}' "
                            f"WHERE user={discord_user_id}")
    connection.commit()
    temp_cursor.close()
    connection.close()
