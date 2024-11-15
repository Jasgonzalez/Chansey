import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Gummy-bears0406',
            database='medicinelog'
        )
        
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None
