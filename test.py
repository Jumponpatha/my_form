from database import create_table, show_table,select_table_statement

# Create user form table
def create_table_user():
    table_script =  '''
                        CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            firstname TEXT NOT NULL,
                            lastname TEXT NOT NULL,
                            email TEXT NOT NULL,
                            phone TEXT NOT NULL,
                            birthdate DATE NOT NULL
                        );               
                    '''

    print(create_table(table_script))
    print(show_table())

if __name__ == "__main__":
    select_table_statement('users')