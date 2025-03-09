import os
import pandas as pd
from meteostat import Daily, Point
from datetime import datetime

# Ensure the data directory exists
DATA_DIR = os.path.join(os.path.dirname(__file__), "../../data/raw/")
os.makedirs(DATA_DIR, exist_ok=True)

# Constants for Melbourne Grand Prix Circuit
LOCATION = Point(-37.8497, 144.968, 7)  # Latitude, Longitude, Elevation (m)

# Australian Grand Prix race dates from 2010 to 2024
race_dates = {
    2024: "2024-03-24",
    2023: "2023-04-02",
    2022: "2022-04-10",
    2019: "2019-03-17",
    2018: "2018-03-25",
    2017: "2017-03-26",
    2016: "2016-03-20",
    2015: "2015-03-15",
    2014: "2014-03-16",
    2013: "2013-03-17",
    2012: "2012-03-18",
    2011: "2011-03-27",
    2010: "2010-03-28",
}

def fetch_weather_data():
    """Fetch historical weather data for Australian Grand Prix race days."""
    weather_data = []

    for year, race_date in race_dates.items():
        date = datetime.strptime(race_date, "%Y-%m-%d")
        data = Daily(LOCATION, date, date).fetch()

        if not data.empty:
            weather_data.append([
                year,
                race_date,
                data["tavg"].iloc[0] if "tavg" in data else None,   # Avg temperature (°C)
                data["prcp"].iloc[0] if "prcp" in data else None,   # Precipitation (mm)
                data["wspd"].iloc[0] if "wspd" in data else None,   # Wind speed (km/h)
                data["pres"].iloc[0] if "pres" in data else None    # Pressure (hPa)
            ])
    
    # Convert to DataFrame
    df = pd.DataFrame(weather_data, columns=["Year", "Date", "Temp_C", "Precip_mm", "Wind_kmh", "Pressure_hPa"])
    
    # Ensure date is properly formatted
    df["Date"] = pd.to_datetime(df["Date"])

    # Save to CSV in the correct directory
    output_path = os.path.join(DATA_DIR, "weather_data.csv")
    df.to_csv(output_path, index=False)
    
    print(f"✅ Weather data saved successfully to {output_path}")

if __name__ == "__main__":
    fetch_weather_data()
