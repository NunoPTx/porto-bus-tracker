import requests
import json
from datetime import datetime

URL = "https://broker.fiware.urbanplatform.portodigital.pt/v2/entities?q=vehicleType==bus&limit=1000"

def run_tracker():
    roster = {}
    try:
        with open("roster.json", "r") as f:
            roster = json.load(f)
    except:
        pass

    try:
        response = requests.get(URL, timeout=30)
        response.raise_for_status()
        buses = response.json()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for bus in buses:
            raw_id = bus.get('id', 'unknown')
            clean_id = raw_id.split(':')[-1]
            roster[clean_id] = now
            
        sorted_keys = sorted(roster.keys(), key=lambda x: int(x) if x.isdigit() else x)
        final_roster = {k: roster[k] for k in sorted_keys}

        with open("roster.json", "w") as f:
            json.dump(final_roster, f, indent=4)
            
        print(f"Updated {len(buses)} buses successfully.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_tracker()
