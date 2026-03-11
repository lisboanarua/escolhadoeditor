import requests
from bs4 import BeautifulSoup
from datetime import datetime

SAPO_URL = "https://www.sapo.pt/"
HTML_FILE = "index.html"

def get_featured_news():
    response = requests.get(SAPO_URL, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    article = soup.select_one("article")
    if not article:
        return None, None

    title = article.get_text(strip=True)
    link = article.find("a")["href"]

    if link.startswith("/"):
        link = "https://www.sapo.pt" + link

    return title, link


def append_to_html(title, link):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    with open(HTML_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    marker = "<ul id=\"news-list\">"

    new_entry = f'\n        <li><a href="{link}" target="_blank">{title}</a> <span class="date">({timestamp})</span></li>'

    updated = content.replace(marker, marker + new_entry)

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(updated)


def main():
    title, link = get_featured_news()
    if title:
        append_to_html(title, link)


if __name__ == "__main__":
    main()
