import json
import requests

import json

with open("driver_stats.json") as file:
    drivers = json.load(file)

print(drivers[0].keys())  # print keys of the first driver dictionary


formatted_drivers = []

for d in drivers:
    formatted_drivers.append({
        "position": int(d.get("POS.") or d.get("Pos") or d.get("pos") or d.get("Position") or d.get("position") or 0),
        "driver": d.get("DRIVER") or d.get("Driver") or d.get("driver"),
        "nationality": d.get("NATIONALITY") or d.get("Nationality") or d.get("nationality"),
        "car": d.get("TEAM") or d.get("Car") or d.get("car"),
        "pts": float(d.get("PTS.") or d.get("PTS") or d.get("pts") or 0),
        "season": int(d.get("Season") or d.get("season") or 0)
    })

response = requests.post("http://localhost:8080/api/drivers/import", json=formatted_drivers)
print(response.status_code, response.text)
