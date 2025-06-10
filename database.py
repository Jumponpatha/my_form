import sqlite3
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# Get the database URL from the environment
db_path = os.getenv("SQLITE_DATABASE_URL")

# Remove "sqlite:///" prefix if needed
if db_path.startswith("sqlite:///"):
    db_file = db_path.replace("sqlite:///", "")
else:
    db_file = db_path

# Ensure the instance directory exists
if not os.path.exists(os.path.dirname(db_file)):
    os.makedirs(os.path.dirname(db_file))
    print(f"Created missing directory: {os.path.dirname(db_file)}")

def sqlite_connection():
    conn = sqlite3.connect(db_path)
    cursor_obj = conn.cursor()
    return conn, cursor_obj

def create_table(table_script):
    conn, cursor_obj = sqlite_connection()
    # Add a table script
    cursor_obj.execute(table_script)
    print("Table is Ready")
    conn.commit()
    # Close the connection
    conn.close()

def select_table_statement(table_name):
    conn, cursor_obj = sqlite_connection()
    # Select table
    statement = f'''SELECT * FROM {table_name};'''
    cursor_obj.execute(statement)
    
    print("All the data:")
    output1 = cursor_obj.fetchmany(10)
    for row in output1:
        print(row)

def select_table_pandas(table_name):
    conn, cursor_obj = sqlite_connection()
    # Select table
    statement = f'''SELECT * FROM {table_name} LIMIT 10;'''
    df = pd.read_sql_query(statement, conn)
    print(df)

def show_table():
    conn, cursor_obj = sqlite_connection()
    # Show table
    statement = f'''SELECT name FROM sqlite_master WHERE type='table';'''
    df = pd.read_sql_query(statement, conn)
    print(df)

def rename_table(old_name, new_name):
    conn, cursor_obj = sqlite_connection()
    # Rename table
    statement = f'''ALTER TABLE {old_name}
                    RENAME TO {new_name};'''
    df = pd.read_sql_query(statement, conn)
    print(df)

def drop_table(table_name):
    conn, cursor_obj = sqlite_connection()
    cursor_obj.execute(f'''DROP TABLE {table_name}''')

