"""Scrape the conference agenda page."""
import requests
from bs4 import BeautifulSoup


def fetch_agenda(url: str) -> list[dict]:
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    events = []  # Placeholder selectors
    for item in soup.select('.agenda-item'):
        title = item.select_one('.title').get_text(strip=True)
        desc = item.select_one('.description').get_text(strip=True)
        events.append({'title': title, 'description': desc})
    return events