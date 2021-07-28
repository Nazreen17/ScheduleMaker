from COREDB.SQLConnection import server_connection
from redacted import SQL_PUBLIC_MAX_TEMPLATE_TABLE
import json
from datetime import datetime


def update_public_max_template(max_schedule, id_num=None, description=None, discord_user_id=None, public=False):
    __check_add_public_max_template_table()
    if public is True and id_num is not None:
        description = description if description is not None else str(datetime.now().date())  # default

    __check_add_public_max_template_record(max_schedule=max_schedule, id_num=id_num, description=description)


def __check_add_public_max_template_table():
    connection = server_connection()
    temp_cursor = connection.cursor()

    temp_cursor.execute(f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name='"
                        f"{SQL_PUBLIC_MAX_TEMPLATE_TABLE}'")

    if temp_cursor.fetchone()[0] != 1:  # fac table does not exist yet, add new fac table
        # ^^^ temp_cursor.fetchone()[0] == 1  # means a table exists
        temp_cursor.execute(f"CREATE TABLE {SQL_PUBLIC_MAX_TEMPLATE_TABLE} "
                            "(id INT NOT NULL AUTO_INCREMENT, description VARCHAR(25) NOT NULL, "
                            "crn_2d_json JSON NOT NULL, PRIMARY KEY(id))")
        connection.commit()
    temp_cursor.close()
    connection.close()


def __check_add_public_max_template_record(max_schedule, id_num, description):
    """
    Void function, adds a MaxSchedule 2D list to the SQL data base at table_name
    :param max_schedule:
    A 2d list of int CRN codes
    :param description:
    25 char long str
    :return:
    """
    connection = server_connection()
    temp_cursor = connection.cursor(buffered=True)

    temp_cursor.execute(f"SELECT * FROM {SQL_PUBLIC_MAX_TEMPLATE_TABLE} WHERE description='{description}'")
    # Select an existing row with matching crn

    # 2D list of integers do not need a custom encoder, just use json.dumps()

    if temp_cursor.rowcount == 0:  # Public MaxSchedule does not exist on a record yet
        temp_cursor.execute(f"INSERT INTO {SQL_PUBLIC_MAX_TEMPLATE_TABLE} (description, crn_2d_json) "
                            f"VALUES ({description}, '{json.dumps(max_schedule)}')")
    else:  # Public MaxSchedule exists, update/overwrite
        temp_cursor.execute(f"UPDATE {SQL_PUBLIC_MAX_TEMPLATE_TABLE} "
                            f"SET crn_2d_json='{json.dumps(max_schedule)}' "
                            f"WHERE id={id_num}")
    connection.commit()
    temp_cursor.close()
    connection.close()
