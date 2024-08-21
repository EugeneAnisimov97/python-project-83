from datetime import datetime
from dotenv import load_dotenv
from psycopg2.extras import NamedTupleCursor
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
        self.cur = self.conn.cursor(cursor_factory=NamedTupleCursor)

    def __enter__(self):
        return self.cur

    def __exit__(self, exc_type, exc_value, traceback):
        self.cur.close()
        self.conn.close()


def get_last_check():
    with DatabaseConnection() as cur:
        cur.execute(
            '''SELECT u.id AS id,
            u.name AS name,
            uc.created_at AS last_check,
            uc.status_code
            FROM urls u
            LEFT JOIN url_checks uc
            ON u.id = uc.url_id
            and uc.id = (SELECT MAX(id)
                        FROM url_checks
                        WHERE url_checks.url_id = u.id)
                        ORDER BY u.id DESC;'''
        )
        return cur.fetchall()


def get_existing_url(base_url):
    with DatabaseConnection() as cur:
        cur.execute('SELECT * FROM urls WHERE name = %s', (base_url,))
        return cur.fetchone()


def insert_url(base_url):
    now = datetime.now()
    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
    with DatabaseConnection() as cur:
        cur.execute(
            '''INSERT INTO urls (name, created_at) VALUES (%s, %s)
            RETURNING id''', (base_url, formatted_now)
        )
        cur.connection.commit()
        return cur.fetchone().id


def filling_data_url(url_id, status_code, h1, title, description):
    now = datetime.now()
    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
    with DatabaseConnection() as cur:
        cur.execute(
            '''INSERT INTO url_checks
            (url_id, status_code, h1, title, description, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)''',
            (url_id, status_code, h1, title, description, formatted_now))
        cur.connection.commit()


def get_url_by_id(url_id):
    with DatabaseConnection() as cur:
        cur.execute('SELECT * FROM urls WHERE id = %s', (url_id,))
        return cur.fetchone()


def get_all_checks(url_id):
    with DatabaseConnection() as cur:
        cur.execute(
            '''select * from url_checks where url_id = %s
            ORDER BY id DESC''', (url_id,)
        )
        return cur.fetchall()
