import mysql.connector

from redacted import SQL_HOST, SQL_USERNAME, SQL_PASSWORD, SQL_DB


def server_connection():
    db_connection = None
    try:
        db_connection = mysql.connector.connect(
            host=SQL_HOST,
            user=SQL_USERNAME,
            passwd=SQL_PASSWORD,
            database=SQL_DB
        )
    except Exception as err:
        print(f"\n\tError: '{err}'")

    return db_connection
