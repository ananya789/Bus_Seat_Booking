import psycopg2
from psycopg2 import Error
from config import DB_CONFIG

def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

def execute_query(conn, query, params=None):
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        return cursor
    except Error as e:
        print(f"Error executing query: {e}")
        conn.rollback()
        return None

def fetch_all(cursor):
    try:
        return cursor.fetchall()
    except Error as e:
        print(f"Error fetching data: {e}")
        return None