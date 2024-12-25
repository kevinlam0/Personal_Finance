from psycopg2 import connect
from psycopg2 import Error as psyError
from psycopg2.extensions import connection, cursor
import os
from dotenv import load_dotenv
import sys
from DataManagers import VenmoReader, Totals_DataDriver, Categorizing


load_dotenv()
# Database configs
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_PORT = os.getenv('DATABASE_PORT')

USER_TABLE_CREATION_SQL = """
    CREATE TABLE IF NOT EXISTS Users (
        user_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        first_name VARCHAR(15),
        last_name VARCHAR(15)
    )
"""

CATEGORY_TABLE_CREATION_SQL = """
    CREATE TABLE IF NOT EXISTS Category (
        category_id SERIAL PRIMARY KEY,
        label VARCHAR(20) NOT NULL,
        user_id BIGINT NOT NULL,
        CONSTRAINT fk_user_category FOREIGN KEY(user_id) REFERENCES Users(user_id),
        CONSTRAINT unique_user_label UNIQUE(user_id, label)
    )
"""
                
def print_psycopg2_exception(err: psyError):
    if err.pgerror == None: return
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno                
    # print the connect() error
    print ("\npsycopg2 ERROR:", err, "on line number:", line_num)
    print ("psycopg2 traceback:", traceback, "-- type:", err_type)

    # psycopg2 extensions.Diagnostics object attribute
    print ("\nextensions.Diagnostics:", err.diag)

    # print the pgcode and pgerror exceptions
    print ("pgerror:", err.pgerror)
    print ("pgcode:", err.pgcode, "\n")
    
def this_connect() -> connection:
    return connect(
            dbname = DATABASE_NAME, 
            user = DATABASE_USER, 
            host = DATABASE_HOST, 
            password = DATABASE_PASSWORD, 
            port = DATABASE_PORT)
    
def create_tables():
    conn: connection = this_connect()
    curs: cursor = conn.cursor()
    try:
        curs.execute(USER_TABLE_CREATION_SQL)
        curs.execute(CATEGORY_TABLE_CREATION_SQL)
        VenmoReader.create_table(conn)
        Totals_DataDriver.create_tables(conn)
        conn.commit()
        print("Successfully created all tables")
    except psyError as e:
        print_psycopg2_exception(e)
        conn.rollback()
    finally:
        curs.close()
        conn.close()
        
def get_venmo_transaction(month: int, year: int):
    return VenmoReader.get_timed_transaction_data(year, month, "../../../cleaner_venmo_data")

def create_categories(user_id: int, labels: list[str]):
    conn = this_connect()
    Categorizing.create_category(conn, user_id, labels)
    conn.close()
    
if __name__ == '__main__':
    # dir_path = "../../../clean_venmo_data"
    # dest_path = "../../../cleaner_venmo_data"
    # VenmoReader.clean_data(dir_path, dest_path)
    # create_tables()
    pass