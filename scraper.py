import requests
from bs4 import BeautifulSoup
import json

UPPER_SIZE_LIMIT = 1000
LOWER_SIZE_LIMIT = 15


def get_tags(url):
    tags = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    ul = soup.find("ul", class_="tags")

    for li in ul.find_all("li", recursive=False):
        tags.append(li.get_text())

    return tags


page = requests.get("http://networkrepository.com/asn.php")
soup = BeautifulSoup(page.content, "html.parser")

networks = []

for row in soup.select("#myTable > tr"):
    cells = row.find_all("td", recursive=False)
    size = int(cells[1]['class'][1][:-1])

    if LOWER_SIZE_LIMIT <= size <= UPPER_SIZE_LIMIT:
        name = cells[0].get_text().strip()
        download = cells[-1].find("a")['href']
        page = "http://networkrepository.com/" + cells[0].find("a")['href']
        tags = get_tags(page)

        entry = {
            'name': name,
            'size': size,
            'download': download,
            'page': page,
            'tags': tags,
        }

        networks.append(entry)

with open("networks-data.json", 'w', encoding='utf-8') as f:
    json.dump(networks, f, ensure_ascii=False, indent=4)
