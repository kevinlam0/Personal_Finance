import psycopg2
import os
from dotenv import load_dotenv
import sys
import VenmoReader

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
        user_id BIGINT,
        CONSTRAINT fk_user_category FOREIGN KEY(user_id) REFERENCES Users(user_id)
    )
"""
                
def print_psycopg2_exception(err):
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
    
def connect():
    return psycopg2.connect(
            database = DATABASE_NAME, 
            user = DATABASE_USER, 
            host = DATABASE_HOST, 
            password = DATABASE_PASSWORD, 
            port = DATABASE_PORT)
    
def create_tables():
    conn = connect()
    curs = conn.cursor()
    try:
        curs.execute(USER_TABLE_CREATION_SQL)
        curs.execute(CATEGORY_TABLE_CREATION_SQL)
        VenmoReader.create_table(conn)
        conn.commit()
    except Exception as e:
        print_psycopg2_exception(e)
        conn.rollback()
    finally:
        curs.close()
        conn.close()
        
if __name__ == '__main__':
    dir_path = "../../../clean_venmo_data"
    dest_path = "../../../cleaner_venmo_data"
    VenmoReader.clean_data(dir_path, dest_path)