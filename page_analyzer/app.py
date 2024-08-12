from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages  # noqa: E501
from dotenv import load_dotenv
from datetime import date
import os
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
    try:
        cur.execute('SELECT * FROM urls WHERE name = %s', (url,))
        already_added_url = cur.fetchone()
        if already_added_url:
            return redirect(url_for('show_url', url_id=already_added_url[0]))
        today = date.today()
        cur.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id', (url, today))  # noqa: E501
        added_url = cur.fetchone()[0]
        conn.commit()
        flash('Страница успешно добавлена.', 'success')
        return redirect(url_for('show_url', url_id=added_url))
    except Exception as e:
        flash(f'Ошибка: {str(e)}', 'error')
        return redirect(url_for('main'))
    finally:
        cur.close()
        conn.close()


@app.route('/urls')
def urls():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM urls ORDER BY created_at DESC')
        urls = cur.fetchall()
        return render_template('urls.html', urls=urls)
    except Exception as e:
        flash(f'Ошибка: {str(e)}', 'error')
        return redirect(url_for('main'))
    finally:
        cur.close()
        conn.close()


@app.route('/urls/<int:url_id>')
def show_url(url_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM urls WHERE id = %s', (url_id,))
        url = cur.fetchone()
        cur.close()
        conn.close()
        if url is None:
            flash('Этот URL не найден.', 'error')
            return redirect(url_for('urls'))
        return render_template('show_url.html', url=url)
    except Exception as e:
        flash(f'Ошибка: {str(e)}', 'error')
        return redirect(url_for('main'))
    finally:
        cur.close()
        conn.close()


if __name__ == '__main__':
    app.run()
