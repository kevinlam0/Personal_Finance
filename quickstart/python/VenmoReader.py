import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
# Database configs
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_PORT = os.getenv('DATABASE_PORT')

TABLE_CREATION_SQL = """CREATE TABLE IF NOT EXISTS VenmoTransaction(
                        transaction_id SERIAL PRIMARY KEY,
                        from VARCHAR(30) NOT NULL,
                        to VARCHAR(30) NOT NULL,
                        note VARCHAR(80) NOT NULL,
                        amount DECIMAL(12,2) NOT NULL,
                        date TIMESTAMP NOT NULL,
                        category_id INT,
                        CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES Category(category_id)
                        )"""


class VenmoReader():
    
    def __init__(self):
        pass

    def connect(self):
        return psycopg2.connect(
            database = DATABASE_NAME, 
            user = DATABASE_USER, 
            host = DATABASE_HOST, 
            password = DATABASE_PASSWORD, 
            port = DATABASE_PORT)
        
    def create_tables(self):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(TABLE_CREATION_SQL)
        conn.commit()
        cur.close()
        conn.close()
        
        