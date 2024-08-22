import validators
from urllib.parse import urlparse


MAX_LENGHT_URL = 255


def get_base_url(url):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url


def validate(url):
    if not validators.url(url):
        return 'Некорректный URL'
    elif len(url) > MAX_LENGHT_URL:
        return f'URL превышает {MAX_LENGHT_URL} символов'
    else:
        return False
