import db_setup
import url_processor

def run_project() -> None:
    """
    This function will run the entire project, starting with setting up the database,
    importing CSV data (if necessary), and then processing URLs with ChatGPT.
    """
    # Step 1: Create the table (if it doesn't exist)
    print("Setting up the database...")
    db_setup.create_table()  # Ensure this function exists in db_setup.py
    
    # Step 2: Import data from the two CSV files into the PostgreSQL table
    print("Importing data from CSV files into the database...")
    
    # Define file paths for the CSV files
    pages_to_db_csv_path = "/Users/manuel/Desktop/JeanPierreWeil_Open_AI/pages_to_db.csv"
    queries_csv_path = "/Users/manuel/Desktop/JeanPierreWeil_Open_AI/queries.csv"
    
    # Import CSV data into the database
    import_csv_to_db(pages_to_db_csv_path)
    import_csv_to_db(queries_csv_path)
    
    # Step 3: Process URLs from the database and analyze with ChatGPT
    print("Processing URLs with ChatGPT and updating the database...")
    url_processor.process_urls()
    
    print("All tasks completed successfully.")

# Define a function to handle importing CSV to the database
def import_csv_to_db(csv_file_path):
    # Add your code to read CSV and insert into the database
    print(f"Importing from {csv_file_path} into the database...")
    # Implement the CSV reading and DB insertion logic here

# This allows us to run the entire process when the script is executed
if __name__ == "__main__":
    run_project()
