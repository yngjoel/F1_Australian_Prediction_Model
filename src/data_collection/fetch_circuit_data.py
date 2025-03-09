import os
import pandas as pd

# Ensure the data directory exists
DATA_DIR = os.path.join(os.path.dirname(__file__), "../../data/raw/")
os.makedirs(DATA_DIR, exist_ok=True)

# Historical fastest lap records at Albert Park Circuit (2010 - 2024)
lap_records = [
    {"Year": 2010, "Driver": "Sebastian Vettel", "Team": "Red Bull", "Lap Time": "1:23.919"},
    {"Year": 2011, "Driver": "Felipe Massa", "Team": "Ferrari", "Lap Time": "1:28.947"},
    {"Year": 2012, "Driver": "Jenson Button", "Team": "McLaren", "Lap Time": "1:29.187"},
    {"Year": 2013, "Driver": "Kimi Räikkönen", "Team": "Lotus", "Lap Time": "1:29.274"},
    {"Year": 2014, "Driver": "Nico Rosberg", "Team": "Mercedes", "Lap Time": "1:32.478"},
    {"Year": 2015, "Driver": "Lewis Hamilton", "Team": "Mercedes", "Lap Time": "1:30.945"},
    {"Year": 2016, "Driver": "Nico Rosberg", "Team": "Mercedes", "Lap Time": "1:28.997"},
    {"Year": 2017, "Driver": "Kimi Räikkönen", "Team": "Ferrari", "Lap Time": "1:26.538"},
    {"Year": 2018, "Driver": "Daniel Ricciardo", "Team": "Red Bull", "Lap Time": "1:25.945"},
    {"Year": 2019, "Driver": "Valtteri Bottas", "Team": "Mercedes", "Lap Time": "1:25.580"},
    {"Year": 2022, "Driver": "Charles Leclerc", "Team": "Ferrari", "Lap Time": "1:20.260"},
    {"Year": 2023, "Driver": "Sergio Pérez", "Team": "Red Bull", "Lap Time": "1:20.235"},
    {"Year": 2024, "Driver": "Max Verstappen", "Team": "Red Bull", "Lap Time": "1:19.870"},  # Placeholder
]

# Circuit details
circuit_info = {
    "Circuit Name": "Albert Park Circuit",
    "Location": "Melbourne, Australia",
    "Type": "Street Circuit",
    "Length (km)": 5.278,
    "Number of Laps": 58,
    "Total Distance (km)": 5.278 * 58,  # Calculate total race distance
    "First Grand Prix": 1996
}

def fetch_circuit_data():
    """Save Albert Park Circuit data and lap records to CSV."""
    # Save circuit details
    circuit_df = pd.DataFrame([circuit_info])
    circuit_df.to_csv(os.path.join(DATA_DIR, "circuit_data.csv"), index=False)

    # Save lap records
    lap_records_df = pd.DataFrame(lap_records)
    lap_records_df.to_csv(os.path.join(DATA_DIR, "lap_records.csv"), index=False)

    print(f"✅ Circuit data and lap records saved successfully in {DATA_DIR}")

if __name__ == "__main__":
    fetch_circuit_data()
