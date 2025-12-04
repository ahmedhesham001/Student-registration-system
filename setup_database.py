import mysql.connector
from mysql.connector import Error

def create_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            port=3307
        )
        if connection.is_connected():
            cursor = connection.cursor()
            
            print("Creating database and tables...")
            with open('db/01_create_tables.sql', 'r') as f:
                sql_script = f.read()
                
            commands = sql_script.split(';')
            for command in commands:
                if command.strip():
                    cursor.execute(command)
            
            print("Tables created successfully.")
            
            print("Inserting dummy data...")
            with open('db/02_insert_data.sql', 'r') as f:
                sql_script = f.read()
                
            commands = sql_script.split(';')
            for command in commands:
                if command.strip():
                    try:
                        print(f"Executing: {command[:50]}...")
                        cursor.execute(command)
                    except Error as e:
                        print(f"Error executing command: {e}")
            
            print("Dummy data inserted successfully.")
            connection.commit()
            
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    create_database()
