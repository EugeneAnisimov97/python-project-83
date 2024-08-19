from bs4 import BeautifulSoup
from urllib.parse import urlparse


def get_url_parsed(url):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url


def parsing_html(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    h1 = soup.find('h1').text if soup.find('h1') else ''
    title = soup.find('title').text if soup.find('title') else ''
    description_tag = soup.find('meta', attrs={'name': 'description'})
    description = description_tag['content'] if description_tag else ''
    return h1, title, description
