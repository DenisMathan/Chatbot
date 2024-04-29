import requests

from bs4 import BeautifulSoup
from helper import splitkeep, filterMinlenght

url = "https://www.quarks.de/gesundheit/koennen-corona-impfungen-spaetfolgen-ausloesen/"

def scrapeURL(url, settings):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()
    if not settings["start"] == None or not settings["end"] == None:
        text = cutOutRelevant(text, settings)
    # print(text)
    text = list(filter( None, text.split("\n")))
    text = filterMinlenght(text, 60)
    print(len(text))
    return text

def cutOutRelevant(text, settings):
    if not settings["start"] == None:
        text = splitkeep(text, settings["start"])
        print(len(text))
        text = text[1]
    if not settings["end"] == None:
        text = splitkeep(text, settings["end"], False)
        print(len(text))
        text = text[0]
    return text

