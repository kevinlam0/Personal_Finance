from psycopg2.extensions import connection, cursor
from psycopg2 import Error as psyError
from . import DatabaseDriver

TOTAL_TABLE = """
    CREATE TABLE IF NOT EXISTS totals (
        user_id BIGINT PRIMARY KEY REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE,
        total_spent DECIMAL(12, 2) DEFAULT 0,
        total_income DECIMAL(12,2) DEFAULT 0
    );
    """

CATEGORY_TOTALS = """
    CREATE TABLE IF NOT EXISTS category_totals (
        user_id BIGINT REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE,
        category_id INT REFERENCES category(category_id) ON UPDATE CASCADE ON DELETE CASCADE,
        total_spent DECIMAL(12,2) DEFAULT 0,
        total_income DECIMAL(12,2) DEFAULT 0,
        PRIMARY KEY (user_id, category_id)
    );
    """

DATE_TOTALS = """
    CREATE TABLE IF NOT EXISTS date_totals (
        user_id BIGINT REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE,
        year INTEGER CHECK(year >= 1990 AND year <= 2100) NOT NULL,
        month INTEGER CHECK(month >= 1 AND month <= 12) NOT NULL,
        total_spent DECIMAL(12, 2) DEFAULT 0,
        total_income DECIMAL(12, 2) DEFAULT 0,
        PRIMARY KEY (user_id, year, month)
    )
    """

def create_tables(conn: connection):
    curs: cursor = conn.cursor()
    try:
        curs.execute(TOTAL_TABLE)
        curs.execute(CATEGORY_TOTALS)
        curs.execute(DATE_TOTALS)
    except psyError as e:
        DatabaseDriver.print_psycopg2_exception(e)
        print("Error creating total tables")
        raise psyError()
    finally:
        curs.close()