from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages  # noqa: E501
from dotenv import load_dotenv
from datetime import date
from bs4 import BeautifulSoup
import os
import psycopg2
import validators
import requests

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
            flash('Страница уже существует', 'info')
            return redirect(url_for('show_url', url_id=already_added_url[0]))
        today = date.today()
        cur.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id', (url, today))  # noqa: E501
        added_url = cur.fetchone()[0]
        conn.commit()
        flash('Страница успешно добавлена', 'success')
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
        check_urls = {}
        for url in urls:
            url_id = url[0]
            cur.execute('select * from url_checks where url_id = %s ORDER BY id DESC LIMIT 1', (url_id,))  # noqa: E501
            last_check = cur.fetchone()
            check_urls[url_id] = last_check
        return render_template('urls.html', urls=urls, check_urls=check_urls)
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
        cur.execute('SELECT * FROM urls WHERE id = %s ORDER BY id DESC', (url_id,))  # noqa: E501
        url = cur.fetchone()
        if url is None:
            flash('Этот URL не найден.', 'error')
            return redirect(url_for('urls'))
        cur.execute('select * from url_checks where url_id = %s ORDER BY id DESC', (url_id,))  # noqa: E501
        check_url = cur.fetchall()
        return render_template('show_url.html', url=url, checks=check_url)
    except Exception as e:
        flash(f'Ошибка: {str(e)}', 'error')
        return redirect(url_for('main'))
    finally:
        cur.close()
        conn.close()


@app.post('/urls/<int:url_id>/checks')
def checks_url(url_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM urls WHERE id = %s', (url_id,))
        url = cur.fetchone()
        if url is None:
            flash('Некорректный URL', 'error')
            return redirect(url_for('urls'))
        response = requests.get(url[1])
        response.raise_for_status()
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            h1 = soup.find('h1').text if soup.find('h1') else ''
            title = soup.find('title').text if soup.find('title') else ''
            description_tag = soup.find('meta', attrs={'name': 'description'})
            description_content = description_tag['content'] if description_tag else ''  # noqa: E501
        else:
            flash('Произошла ошибка при проверке')
            return redirect(url_for('show_url', url_id=url_id))
        today = date.today()
        cur.execute('INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at) VALUES (%s, %s, %s, %s, %s, %s)', (url_id, response.status_code, h1, title, description_content, today))  # noqa: E501
        conn.commit()
        flash('Страница успешно проверена', 'success')
        return redirect(url_for('show_url', url_id=url_id))
    except Exception as e:
        flash(f'Ошибка: {str(e)}', 'error')
        return redirect(url_for('main'))
    finally:
        cur.close()
        conn.close()


if __name__ == '__main__':
    app.run(debug=True)
