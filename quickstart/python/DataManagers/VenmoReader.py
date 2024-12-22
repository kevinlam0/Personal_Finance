from psycopg2.extensions import connection, cursor
from psycopg2 import Error as psyError
import os
import DatabaseDriver
import pandas as pd
import re

TABLE_CREATION_SQL = """
    CREATE TABLE IF NOT EXISTS VenmoTransaction(
        user_id BIGINT,
        transaction_id BIGINT,
        sender VARCHAR(30) NOT NULL,
        recipient VARCHAR(30) NOT NULL,
        note TEXT NOT NULL,
        amount DECIMAL(12,2) NOT NULL,
        date_time TIMESTAMP NOT NULL,
        category_id INT,
        CONSTRAINT fk_userid FOREIGN KEY (user_id) REFERENCES Users(user_id),
        CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES Category(category_id),
        PRIMARY KEY (user_id, transaction_id)
    )
"""

def create_table(conn: connection):
    cur: cursor = conn.cursor()
    try:
        cur.execute(TABLE_CREATION_SQL)
        conn.commit()
    except psyError as e:
        DatabaseDriver.print_psycopg2_exception(e)
        print("Exception occurred creating Venmo table")
        raise psyError()
    finally:
        cur.close()

def find_columns(df: pd.DataFrame, max_rows_to_search = 5):
    count_col = 0
    indices = {"id": None, "datetime": None, "note": None, "from": None, "to": None, "amount (total)": None} #id, datetime, note, from, to, amount
    
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
            return indices
        # Iterate row counter to make sure we don't search too many rows
        if i == max_rows_to_search:
            break
    raise Exception("Error finding column indicies: did not find all indicies before max rows to search")
        
        

        
def clean_data(src_dir: str, dest_dir: str):
    """ Gets rid of the rows and columns that are not needed in the raw Venmo CSV exports and create new csv files

    Args:
        directory (str): directory must contain .csv files that only pertain to the Venmo export formats
    """
    os.makedirs(dest_dir, exist_ok=True)
    
    paths: list[str] = os.listdir(src_dir)

    for file in paths:
        if not file.endswith(".csv"): continue
        
        # Dropping unwanted column and rows
        df = pd.read_csv(f"{src_dir}/{file}", header=None)
        col_indices = find_columns(df)
        df = df.dropna(subset=[df.columns[col_indices["from"]]]).reset_index(drop=True)
        df = df.iloc[:, list(col_indices.values())]
        # Cleaning currency
        df = df.rename(columns={'Amount (total)': 'Amount'}, errors='raise')
        df['Amount'] = df['Amount'].str.replace(r'[^\d.-]', '', regex=True)
        
        # Making column header
        df.columns = df.iloc[0]
        df.drop(0, axis=0, inplace=True)
        
        # File naming
        year_match = re.search(r"(19|20)\d{2}", file)
        month_match = re.search(r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)", file, re.IGNORECASE)
        
        if not year_match or not month_match:
            print("Did not find file naming dates")
            return
        
        file_name = f"{year_match.group(0)}{month_match.group(0)}_cleanVenmo.csv"
        file_path = os.path.join(dest_dir, file_name)
        df.to_csv(file_path, index = False)