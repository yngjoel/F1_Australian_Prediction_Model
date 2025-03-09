import requests
import pandas as pd

# Function to fetch pit stop data from Ergast API
def get_pit_stop_data(season, race_round):
    url = f'http://ergast.com/api/f1/{season}/{race_round}/pitstops.json'
    response = requests.get(url)
    data = response.json()

    # Check if race data is available
    if 'MRData' in data and 'RaceTable' in data['MRData'] and 'Races' in data['MRData']['RaceTable']:
        races = data['MRData']['RaceTable']['Races']
        if races:
            # Extract pit stop data if available
            pit_stops = races[0].get('PitStops', [])
            if pit_stops:
                df_pit_stops = pd.json_normalize(pit_stops)
                return df_pit_stops
            else:
                print(f"No pit stop data available for {season} round {race_round}.")
                return pd.DataFrame()  # Return an empty DataFrame if no pit stops
        else:
            print(f"No race data available for {season} round {race_round}.")
            return pd.DataFrame()  # Return an empty DataFrame if no race data
    else:
        print(f"Invalid data structure for {season} round {race_round}.")
        return pd.DataFrame()  # Return an empty DataFrame if the structure is invalid

# Example: Fetch pit stop data for the 2024 Australian GP (race round 3)
df_pit_stops = get_pit_stop_data(2024, 3)

# Check if data is available before saving
if not df_pit_stops.empty:
    df_pit_stops.to_csv('data/processed/pit_stop_data_2024_australia.csv', index=False)
else:
    print("No pit stop data to save.")
