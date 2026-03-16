import requests
import json
from datetime import datetime

URL = "https://broker.fiware.urbanplatform.portodigital.pt/v2/entities?q=vehicleType==bus&limit=1000"

def run_tracker():
    # 1. Load the existing roster (memory of the fleet)
    roster = {}
    try:
        with open("roster.json", "r") as f:
            # We load the existing dictionary
            roster = json.load(f)
    except:
        # If the file doesn't exist yet, we just start with an empty dictionary
        pass

    # 2. Get the new live data
    try:
        response = requests.get(URL, timeout=30)
        response.raise_for_status()
        buses = response.json()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 3. Update the dictionary with current findings
        for bus in buses:
            raw_id = bus.get('id', 'unknown')
            clean_id = raw_id.split(':')[-1]
            # This updates the time for the ID, or adds it if it's new
            roster[clean_id] = now

        # 4. ORDER BY ID (Numerical)
        # This prevents the file from growing into a long "list" of repeated IDs
        # It keeps exactly one entry per bus number, sorted 1, 2, 3...
        sorted_keys = sorted(roster.keys(), key=lambda x: int(x) if x.isdigit() else x)
        final_roster = {k: roster[k] for k in sorted_keys}

        # 5. OVERWRITE the old file with the fresh, sorted dictionary
        with open("roster.json", "w") as f:
            json.dump(final_roster, f, indent=4)
            
        print(f"Updated {len(buses)} buses successfully.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_tracker()
