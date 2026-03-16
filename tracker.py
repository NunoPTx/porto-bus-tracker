import requests
import json
from datetime import datetime

# The Porto API URL
URL = "https://broker.fiware.urbanplatform.portodigital.pt/v2/entities?q=vehicleType==bus&limit=1000"

def run_tracker():
    # 1. Load the existing roster
    try:
        with open("roster.json", "r") as f:
            roster = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        roster = {}

    # 2. Fetch live data
    try:
        print("Fetching data from Porto API...")
        response = requests.get(URL, timeout=30)
        response.raise_for_status() # Check if the website is actually working
        buses = response.json()
        
        # Get the current time in Porto
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 3. Update the roster
        for bus in buses:
            # We use the ID as the key, and the time as the value
            bus_id = bus.get('id', 'unknown')
            roster[bus_id] = now

        # 4. Sort the roster by date (oldest first) before saving
        # This makes it easy to see "Retired" buses at the top of the file
        sorted_roster = dict(sorted(roster.items(), key=lambda item: item[1]))

        # 5. Save the updated roster
        with open("roster.json", "w") as f:
            json.dump(sorted_roster, f, indent=4)
            
        print(f"Success! Tracked {len(buses)} buses at {now}.")

    except Exception as e:
        print(f"Failed to update: {e}")

if __name__ == "__main__":
    run_tracker()
