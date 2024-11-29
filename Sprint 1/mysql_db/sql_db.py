# imports database from mysql 
import mysql.connector
from mysql.connector import Error

def create_db_and_connection():
    #creates connection to MySql db and returns object

    try:
        connection = mysql.connector.connect(
            host='chansey-db.c1es26gc2k7l.us-east-2.rds.amazonaws.com',
            user='admin',
            password = 'ch8trabrabru',
            database = 'chansey-db'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS chansey-db")
            connection.database = 'chansey-db' 
            #this will switch to the new database

            print("Database 'chansey-db' created or already exists.")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None
    
conn = create_db_and_connection()
if conn:

    #operations to use database will be here
   def create_entry(connection, medicine_data):
        cursor = connection.cursor()
        sql = "INSERT INTO chansey-db (medname, medtype, startdate, freq, alarmtime) VALUES (%s, %s, %d, %s, %d)"
        medicineval = input ("Enter medicine name:")
        medtype = input("Enter type of medicine")
        startdate = input("Enter start date")
        freq = input("Enter frequency of dose")
        alarmtime = input("Enter a time to remind you to take dose:")

        cursor.execute(sql, medicineval, medtype, startdate, freq, alarmtime) 

        connection.commit()

conn.close()
