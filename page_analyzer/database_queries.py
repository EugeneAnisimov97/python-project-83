from datetime import date
from meneger import DatabaseConnection


today = date.today()


def get_all_urls():
    with DatabaseConnection() as cur:
        cur.execute('SELECT * FROM urls ORDER BY created_at DESC')
        return cur.fetchall()


def get_last_check(url_id):
    with DatabaseConnection() as cur:
        cur.execute('SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC LIMIT 1', (url_id,))  # noqa: E501
        return cur.fetchone()


def get_existing_url(base_url):
    with DatabaseConnection() as cur:
        cur.execute('SELECT * FROM urls WHERE name = %s', (base_url,))
        return cur.fetchone()


def add_url(base_url, today=today):
    with DatabaseConnection() as cur:
        cur.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id', (base_url, today))  # noqa: E501
        cur.connection.commit()
        return cur.fetchone()[0]


def filling_data_url(url_id, status_code, h1, title, description_content, today=today):  # noqa: E501
    with DatabaseConnection() as cur:
        cur.execute('INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at) VALUES (%s, %s, %s, %s, %s, %s)', (url_id, status_code, h1, title, description_content, today))  # noqa: E501
        cur.connection.commit()


def search_url(url_id):
    with DatabaseConnection() as cur:
        cur.execute('SELECT * FROM urls WHERE id = %s', (url_id,))
        return cur.fetchone()


def get_all_check(url_id):
    with DatabaseConnection() as cur:
        cur.execute('select * from url_checks where url_id = %s ORDER BY id DESC', (url_id,))  # noqa: E501
        return cur.fetchall()
