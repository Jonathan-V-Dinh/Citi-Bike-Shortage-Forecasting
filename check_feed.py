import json
from datetime import datetime, timezone
from urllib.request import urlopen


def fetch(url):
    with urlopen(url, timeout=20) as response:
        return json.load(response)


directory = fetch("https://gbfs.citibikenyc.com/gbfs/gbfs.json")
feeds = {item["name"]: item["url"] for item in directory["data"]["en"]["feeds"]}
status = fetch(feeds["station_status"])
info = fetch(feeds["station_information"])
stations = status["data"]["stations"]
names = {row["station_id"]: row["name"] for row in info["data"]["stations"]}

active = [
    row for row in stations
    if row["is_installed"] and row["is_renting"] and row["is_returning"]
]
updated = datetime.fromtimestamp(status["last_updated"], timezone.utc)
print(f"Feed updated: {updated.isoformat()}")
print(f"{len(stations):,} stations, {len(active):,} open for pickups and returns")
print(f"{sum(row['num_bikes_available'] == 0 for row in active):,} open stations with zero bikes")
for row in active[:10]:
    name = names.get(row["station_id"], row["station_id"])
    print(f"{name}: {row['num_bikes_available']} bikes, {row['num_docks_available']} open docks")
