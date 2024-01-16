import requests

from bs4 import BeautifulSoup
from helper import splitkeep, filterMinlenght

url = "https://www.quarks.de/gesundheit/koennen-corona-impfungen-spaetfolgen-ausloesen/"
def scrapeURL(url, settings):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()
    text = list(filter( None, text.split("\n")))
    text = filterMinlenght(text, 60)
    print(len(text))
    return text