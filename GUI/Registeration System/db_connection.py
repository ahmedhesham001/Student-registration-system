import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  
            password='1234',  
            database='student_registration_system',
            port=3307
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

if __name__ == '__main__':
    conn = get_db_connection()
    if conn:
        print("Connection successful!")
        conn.close()
