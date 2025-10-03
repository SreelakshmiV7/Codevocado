import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="SRee@2004",  # replace with your password
        database="crud_db"
    )
