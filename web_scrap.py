import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_wikipedia(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Unable to access page: {url}")
    
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find('h1', id="firstHeading").text

    first_paragraph = soup.find('div', class_='mw-parser-output').find('p').text

    external_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('http'):
            external_links.append(href)

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

if __name__ == "__main__":
    wikipedia_url = "https://en.wikipedia.org/wiki/Web_scraping"
    data = scrape_wikipedia(wikipedia_url)
    
    print(f"Title: {data['title']}\n")
    print(f"First Paragraph: {data['first_paragraph']}\n")
    print(f"External Links: {data['external_links']}\n")
    print(f"Images: {data['images']}\n")

