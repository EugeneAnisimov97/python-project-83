from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    get_flashed_messages,
    abort
)
from dotenv import load_dotenv
from page_analyzer.validator import validate, get_base_url
from page_analyzer.database import (
    get_last_check,
    get_existing_url,
    insert_new_url,
    insert_url_check_data,
    get_url_by_id,
    get_all_checks
)
from page_analyzer.parser import parse_html
import requests
import os

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    """Home page route handler"""
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages)


@app.post('/urls')
def create_url():
    """handler for adding a page to the database"""
    url = request.form.get('url')
    if validate(url):
        error = validate(url)
        flash(error, 'danger')
        return render_template('index.html'), 422
    base_url = get_base_url(url)
    already_added_url = get_existing_url(base_url)
    if already_added_url:
        flash('Страница уже существует', 'info')
        return redirect(url_for('show_url', url_id=already_added_url.id))
    added_url = insert_new_url(base_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('show_url', url_id=added_url))


@app.route('/urls')
def urls():
    """display handler added to the page database"""
    last_check = get_last_check()
    return render_template('urls.html', check_urls=last_check)


@app.route('/urls/<int:url_id>')
def show_url(url_id):
    """A handler for displaying information about a specific URL"""
    url = get_url_by_id(url_id)
    if url is None:
        flash('Этот URL не найден.', 'danger')
        abort(404)
    check_url = get_all_checks(url_id)
    return render_template('show_url.html', url=url, checks=check_url)


@app.post('/urls/<int:url_id>/checks')
def checks_url(url_id):
    """A handler for displaying a check about a specific URL"""
    url = get_url_by_id(url_id)
    try:
        response = requests.get(url.name)
        response.raise_for_status()
    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('show_url', url_id=url_id))
    parsed_html = parse_html(response)
    insert_url_check_data(
        url_id,
        response.status_code,
        parsed_html
    )
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('show_url', url_id=url_id))


@app.errorhandler(404)
def not_found(error):
    """Handler for displaying a page when an error occurs 404"""
    return render_template('error.html',
                           error='404 - Страница не найдена',
                           code=404), 404


@app.errorhandler(500)
def internal_error(error):
    """Handler for displaying a page when an error occurs 500"""
    return render_template('error.html',
                           error='500 - Внутрення ошибка сервера',
                           code=500), 500


if __name__ == '__main__':
    app.run(debug=True)
