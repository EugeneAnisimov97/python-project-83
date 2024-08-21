from bs4 import BeautifulSoup


def parsing_html(response):
    parsed_html = {}
    soup = BeautifulSoup(response.content, 'html.parser')
    parsed_html['h1'] = soup.find('h1').text if soup.find('h1') else ''
    parsed_html['title'] = soup.find('title').text if soup.find('title') else ''
    desc_tag = soup.find('meta', attrs={'name': 'description'})
    parsed_html['description'] = desc_tag['content'] if desc_tag else ''
    return parsed_html
