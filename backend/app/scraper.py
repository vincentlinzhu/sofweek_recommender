import json
import requests
from bs4 import BeautifulSoup

def _parse_ldjson(soup: BeautifulSoup) -> list[dict]:
    """Extract events from JSON-LD blocks if available."""
    events: list[dict] = []
    for script in soup.find_all("script", {"type": "application/ld+json"}):
        try:
            data = json.loads(script.string or "")
        except json.JSONDecodeError:
            continue

        items = []
        if isinstance(data, dict):
            if data.get("@type") == "Event":
                items.append(data)
            elif isinstance(data.get("@graph"), list):
                items.extend([i for i in data["@graph"] if i.get("@type") == "Event"])
        elif isinstance(data, list):
            items.extend([i for i in data if isinstance(i, dict) and i.get("@type") == "Event"])

        for item in items:
            title = item.get("name")
            description = BeautifulSoup(item.get("description", ""), "html.parser").get_text(" ", strip=True)
            start = item.get("startDate")
            location = None
            if isinstance(item.get("location"), dict):
                location = item["location"].get("name")

            performers = item.get("performer") or []
            if isinstance(performers, dict):
                performers = [performers]
            speakers = [p.get("name") for p in performers if isinstance(p, dict) and p.get("name")]

            events.append(
                {
                    "title": title,
                    "description": description,
                    "starts_at": start,
                    "location": location,
                    "speakers": speakers,
                }
            )

    return events

def fetch_agenda(url: str) -> list[dict]:
    """Fetch and parse agenda information from the provided URL."""
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # First try JSON-LD structured data which many modern sites expose.
    events = _parse_ldjson(soup)
    if events:
        return events

    # Fallback: attempt to parse common agenda markup patterns.
    for item in soup.select(
        ".agenda-item, .event, .tribe-events-calendar-list__event"
    ):
        title_elem = item.select_one(
            ".title, .event-title, .tribe-events-calendar-list__event-title"
        )
        desc_elem = item.select_one(
            ".description, .tribe-events-calendar-list__event-description, .event-description"
        )
        time_elem = item.select_one("time[datetime]")
        loc_elem = item.select_one(
            ".location, .tribe-events-venue-details, .event-location"
        )
        speaker_elems = item.select(
            ".speaker, .tribe-events-speaker, .event-speaker"
        )

        events.append(
            {
                "title": title_elem.get_text(strip=True) if title_elem else None,
                "description": desc_elem.get_text(strip=True) if desc_elem else None,
                "starts_at": time_elem.get("datetime") if time_elem else None,
                "location": loc_elem.get_text(strip=True) if loc_elem else None,
                "speakers": [s.get_text(strip=True) for s in speaker_elems],
            }
        )
    
    return events