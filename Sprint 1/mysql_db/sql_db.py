# imports database from mysql 
import mysql.connector
from mysql.connector import Error

def create_db_and_connection():
    #creates connection to MySql db and returns object

    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='leonkat355',
            password = 'chansey#355'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS medicinelog")
            connection.database = 'medicinelog' 
            #this will switch to the new database

            print("Database 'medicinelog' created or already exists.")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None
    
conn = create_db_and_connection()
#if conn:

    #operations to use database will be here
   # def create_entry(connection, medicine_data):
      #  cursor = connection.cursor()
     #   sql_insert_query = 

            
    

    #conn.close()

