from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages  # noqa: E501
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from page_analyzer.validator import validate
from page_analyzer.database_queries import get_all_urls, get_last_check, get_existing_url, add_url, filling_data_url, search_url, get_all_check  # noqa: E501
import requests
import os

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def main():
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages)


@app.post('/urls')
def post_main():
    url = request.form.get('url')
    if validate(url):
        flash('Некорректный URL', 'danger')
        return render_template('index.html'), 422
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    already_added_url = get_existing_url(base_url)
    if already_added_url:
        flash('Страница уже существует', 'info')
        return redirect(url_for('show_url', url_id=already_added_url[0]))
    added_url = add_url(base_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('show_url', url_id=added_url))


@app.route('/urls')
def urls():
    urls = get_all_urls()
    check_urls = {}
    for url in urls:
        url_id = url[0]
        last_check = get_last_check(url_id)
        check_urls[url_id] = last_check
    return render_template('urls.html', urls=urls, check_urls=check_urls)


@app.route('/urls/<int:url_id>')
def show_url(url_id):
    url = search_url(url_id)
    if url is None:
        flash('Этот URL не найден.', 'danger')
        return redirect(url_for('urls'))
    check_url = get_all_check(url_id)
    return render_template('show_url.html', url=url, checks=check_url)


@app.post('/urls/<int:url_id>/checks')
def checks_url(url_id):
    try:
        url = search_url(url_id)
        if url is None:
            flash('URL не найден!', 'danger')
            return redirect(url_for('urls'))
        response = requests.get(url[1])
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        h1 = soup.find('h1').text if soup.find('h1') else ''
        title = soup.find('title').text if soup.find('title') else ''
        description_tag = soup.find('meta', attrs={'name': 'description'})
        description_content = description_tag['content'] if description_tag else ''  # noqa: E501
        filling_data_url(url_id, response.status_code, h1, title, description_content)  # noqa: E501
        flash('Страница успешно проверена', 'success')
        return redirect(url_for('show_url', url_id=url_id))
    except Exception:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('show_url', url_id=url_id))


if __name__ == '__main__':
    app.run(debug=True)
