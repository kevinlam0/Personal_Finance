import psycopg2
import os
from dotenv import load_dotenv
import DatabaseDriver
import pandas as pd
from math import isnan


load_dotenv()
# Database configs
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_PORT = os.getenv('DATABASE_PORT')

TABLE_CREATION_SQL = """CREATE TABLE IF NOT EXISTS VenmoTransaction(
                        transaction_id SERIAL PRIMARY KEY,
                        sender VARCHAR(30) NOT NULL,
                        recipient VARCHAR(30) NOT NULL,
                        note VARCHAR(80) NOT NULL,
                        amount DECIMAL(12,2) NOT NULL,
                        date TIMESTAMP NOT NULL,
                        category_id INT,
                        CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES Category(category_id)
                        )"""


def find_columns(df: pd.DataFrame, max_rows_to_search = 5):
    count_col = 0
    indices = {"id": None, "datetime": None, "note": None, "from": None, "to": None, "amount (total)": None} #id, datetime, note, from, to, amount
    count_row = 0
    
    # Iterate through the rows of the df
    for i, row in df.iterrows():
        # Iterate through the columns of the row
        for col_i, val in enumerate(row):
            try:
                if val.lower() in indices:
                    indices[val.lower()] = col_i
                    count_col += 1
            
            except AttributeError: # val can be NaN, so it raises this error during val.lower()
                continue
            
        # If we found all columns needed, return
        if count_col == len(indices):
            return indices, count_row
        # Iterate row counter to make sure we don't search too many rows
        count_row += 1
        if count_row == max_rows_to_search:
            break
    raise Exception("Error finding column indicies: did not find all indicies before max rows to search")
    
    
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
        try:
            cur.execute(TABLE_CREATION_SQL)
            conn.commit()
        except Exception as e:
            DatabaseDriver.print_psycopg2_exception(e)
            conn.rollback()
        finally:
            cur.close()
            conn.close()
            
    
            
    def clean_data(self, directory: str):
        """ Gets rid of the rows and columns that are not needed in the raw Venmo CSV exports and create new csv files

        Args:
            directory (str): directory must contain .csv files that only pertain to the Venmo export formats
        """
        
        paths: list[str] = os.listdir(directory)
        for file in paths:
            if not file.endswith(".csv"): continue
            
            df = pd.read_csv(f"{directory}/{file}")
            col_indices, last_row = find_columns(df)
            
            
        return
        for file in paths:
            if not file.endswith(".csv"): continue
    
    
        
if __name__ == '__main__':
       vr = VenmoReader()
       dir_path = "../../../Finance_Tracker/venmoData"
       vr.clean_data(dir_path)