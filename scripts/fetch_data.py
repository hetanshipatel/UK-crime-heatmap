import requests
import pandas as pd
import time
from datetime import datetime

# Cities with known valid coordinates supported by UK Police API
cities = {
    "London": {"lat": 51.5074, "lng": -0.1278},         # Westminster
    "Manchester": {"lat": 53.4808, "lng": -2.2426},
    "Birmingham": {"lat": 52.4862, "lng": -1.8904},
    "Leeds": {"lat": 53.8008, "lng": -1.5491},
    "Sheffield": {"lat": 53.3811, "lng": -1.4701}
}

# Set the month you want to fetch crime data for
latest_month = "2024-12"  # Format: YYYY-MM

def fetch_crime_data(city, lat, lng, date):
    """Fetch crime data from UK Police API for a given city and month"""
    url = f"https://data.police.uk/api/crimes-street/all-crime?lat={lat}&lng={lng}&date={date}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            crimes = response.json()
            for crime in crimes:
                crime["city"] = city
            return crimes
        else:
            print(f"❌ Failed for {city}: HTTP {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Exception for {city}: {e}")
        return []

def main():
    all_crimes = []
    print(f"\n🔎 Fetching crime data for {latest_month} ...\n")
    for city, coords in cities.items():
        print(f"📍 Fetching crime data for {city} ({latest_month}) ...")
        data = fetch_crime_data(city, coords["lat"], coords["lng"], latest_month)
        if data:
            all_crimes.extend(data)
        time.sleep(1)  # to avoid hitting the API too fast

    if all_crimes:
        df = pd.DataFrame(all_crimes)
        df.to_csv("data/uk_crime_data.csv", index=False)
        print(f"\n✅ Crime data saved to 'data/uk_crime_data.csv'")
        print(f"📊 Total records: {len(df)}\n")
    else:
        print("\n❌ No data was collected.\n")

if __name__ == "__main__":
    main()
