import mysql.connector
from mysql.connector import Error

def update_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='student_registration_system',
            port=3307
        )
        if connection.is_connected():
            cursor = connection.cursor()
            
            # 1. Add columns (Execute 03_alter_tables.sql)
            print("Adding columns...")
            try:
                with open('db/03_alter_tables.sql', 'r') as f:
                    sql_script = f.read()
                commands = sql_script.split(';')
                for command in commands:
                    if command.strip():
                        try:
                            cursor.execute(command)
                        except Error as e:
                            print(f"Warning executing command: {e}") # Might fail if columns already exist
            except FileNotFoundError:
                print("03_alter_tables.sql not found.")

            # 2. Update existing courses with code and credit
            print("Updating enrollment data...")
            # Mapping based on the order in 02_insert_data.sql
            # Existing IDs are 101 to 115
            enrollment_updates = [
                ('2023-01-15'),
                ('2023-02-20'),
                ('2023-03-10'),
                ('2023-04-05'),
                ('2023-05-25'),
                ('2023-06-30'),
                ('2023-07-12'),
                ('2023-08-18'),
                ('2023-09-22'),
                ('2023-10-08'),
                ('2023-11-14'),
                ('2023-12-01'),
                ('2024-01-28'),
                ('2024-02-15'),
                ('2024-03-20')
            ]
            
            start_id = 1001
            for i, enrollment_date in enumerate(enrollment_updates):
                enrollment_id = start_id + i
                cursor.execute(
                    "UPDATE enrollments SET enrollment_date = %s WHERE id = %s",
                    (enrollment_date, enrollment_id)
                )
            
            connection.commit()
            print("Database updated successfully.")
            
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    update_database()
