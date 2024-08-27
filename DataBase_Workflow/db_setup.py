import csv
import psycopg2
from psycopg2 import sql
from env_loader import load_env_vars
import pandas as pd

def create_table() -> None:
    """
    Creates the 'identify_duplicates' table in the PostgreSQL database if it doesn't exist.
    """
    env_vars = load_env_vars()

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname=env_vars['DB_NAME'],
        user=env_vars['DB_USER'],
        password=env_vars['DB_PASSWORD'],
        host=env_vars['DB_HOST'],
        port=env_vars['DB_PORT']
    )
    
    cursor = conn.cursor()

    # SQL command to create a new table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS identify_duplicates (
        URL TEXT PRIMARY KEY,
        Clicks INTEGER,
        Impressions INTEGER,
        CTR TEXT,
        Position TEXT,
        Topics TEXT
    );
    """
    
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()
    print("Table 'identify_duplicates' is set up successfully.")

def import_csv_to_db(csv_file_path):
    """Function to read a CSV file and insert data into the identify_duplicates table."""
    try:
        # Load environment variables for DB credentials
        env_vars = load_env_vars()

        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname=env_vars['DB_NAME'],
            user=env_vars['DB_USER'],
            password=env_vars['DB_PASSWORD'],
            host=env_vars['DB_HOST'],
            port=env_vars['DB_PORT']
        )

        cursor = conn.cursor()
        
        # with open(csv_file_path, 'r') as file:
        #     csv_reader = csv.reader(file)
        #     next(csv_reader)  # Skip header row if present

        #     for row in csv_reader:
        #         # Adjust column names and number of values to match your table structure
        #         cursor.execute(
        #             "INSERT INTO identify_duplicates (URL, Topics, Visits, Impressions, CTR, Ranking) VALUES (%s, %s, %s, %s, %s, %s)",
        #             row
        #         )

        df = pd.read_csv(csv_file_path)
        df = df.where(pd.notnull(df), None)
        data_tuples = list(df.itertuples(index=False, name=None))
        for row in data_tuples:
            print(row)
            row_tuple = tuple(row)
            
            cursor.execute(
                "INSERT INTO identify_duplicates (URL, Clicks, Impressions, CTR, Position, Topics) VALUES (%s, %s, %s, %s, %s, %s)", 
                row_tuple
            )

        # Commit the changes
        conn.commit()
        print(f"Data from {csv_file_path} imported successfully!")

    except Exception as e:
        print(f"An error occurred while importing data from {csv_file_path}: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    create_table()
    csv_file_path = "/Users/manuel/Desktop/JeanPierreWeil_Open_AI/url_data.csv"
    import_csv_to_db(csv_file_path)
    # You can add additional calls to import_csv_to_db() if needed
