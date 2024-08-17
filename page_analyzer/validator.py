import validators


def validate(url):
    if not url or len(url) > 255 or not validators.url(url):
        return True
