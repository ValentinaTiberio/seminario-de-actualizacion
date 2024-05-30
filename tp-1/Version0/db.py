import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='tp-1',
            port='3306'
        )
        if connection.is_connected():
            print('Connected to the database.')
            return connection
    except Error as e:
                print('Error connecting to the database:', e)
    return None

db = create_connection()