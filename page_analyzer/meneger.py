from dotenv import load_dotenv
# from psycopg2.extras import NamedTupleCursor
import psycopg2
import os


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


class DatabaseConnection:
    def __init__(self):
        self.conn = get_db_connection()
        self.cur = self.conn.cursor()

    def __enter__(self):
        return self.cur

    def __exit__(self, exc_type, exc_value, traceback):
        self.cur.close()
        self.conn.close()
