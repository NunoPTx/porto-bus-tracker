import requests
import json
from datetime import datetime

URL = "https://broker.fiware.urbanplatform.portodigital.pt/v2/entities?q=vehicleType==bus&limit=1000"

def run_tracker():
    try:
        with open("roster.json", "r") as f:
            roster = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        roster = {}

    try:
        response = requests.get(URL, timeout=30)
        response.raise_for_status()
        buses = response.json()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for bus in buses:
            raw_id = bus.get('id', 'unknown')
            # This turns "urn:ngsi-ld:Vehicle:STCP:3205" into just "3205"
            clean_id = raw_id.split(':')[-1]
            roster[clean_id] = now

        # Sort so the oldest (retired) buses stay at the TOP
        sorted_roster = dict(sorted(roster.items(), key=lambda item: item[1]))

        with open("roster.json", "w") as f:
            json.dump(sorted_roster, f, indent=4)
            
        print(f"Success! Updated {len(buses)} buses.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_tracker()
