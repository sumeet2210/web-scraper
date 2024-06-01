import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def scrape_wikipedia(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to load page {url}")

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract Page Title
    title = soup.find('h1', id="firstHeading").text

    # Extract First Paragraph
    first_paragraph = soup.find('div', class_='mw-parser-output').find('p').text

    # Extract External Links
    external_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('http'):
            external_links.append(href)

    # Extract Images and their alt text or captions
    images = []
    for img in soup.find_all('img'):
        img_url = urljoin(url, img['src'])
        img_alt = img.get('alt', '')
        images.append({'url': img_url, 'alt': img_alt})

    return {
        'title': title,
        'first_paragraph': first_paragraph,
        'external_links': external_links,
        'images': images
    }

