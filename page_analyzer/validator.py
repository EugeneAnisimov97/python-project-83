import validators
from urllib.parse import urlparse


def get_url_parsed(url):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url


def validate(url):
    if not validators.url(url):
        return f'Некорректный URL'
    elif len(url) > 255:
        return f'URL слишком длинный'
    else:
        return False
