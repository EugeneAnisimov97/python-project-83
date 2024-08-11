from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages  # noqa: E501
import os
from dotenv import load_dotenv
import psycopg2
import validators

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


@app.route('/')
def main():
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages)


@app.post('/urls')
def post_main():
    url = request.form.get('url')
    if not url or len(url) > 255 or not validators.url(url):
        flash('Некорректный URL', 'error')
        return redirect(url_for('main'))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO urls (name) VALUES (%s) RETURNING id', (url,))
    added_url = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    flash('Страница успешно добавлена.', 'success')
    return redirect(url_for('show_url', url_id=added_url))


@app.route('/urls')
def urls():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM urls ORDER BY created_at DESC')
    urls = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:url_id>')
def show_url(url_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM urls WHERE id = %s', (url_id,))
    url = cur.fetchone()
    cur.close()
    conn.close()
    if url is None:
        flash('Этот URL не найден.', 'error')
        return redirect(url_for('urls'))
    return render_template('show_url.html', url=url)


if __name__ == '__main__':
    app.run()
