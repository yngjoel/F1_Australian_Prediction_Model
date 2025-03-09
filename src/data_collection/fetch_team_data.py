import requests
import pandas as pd

# Function to fetch team data (constructor standings) from Ergast API
def get_team_data(season):
    url = f'http://ergast.com/api/f1/{season}/constructorStandings.json'
    response = requests.get(url)
    data = response.json()

    # Check if data exists and contains the necessary structure
    if 'MRData' in data and 'StandingsTable' in data['MRData'] and 'StandingsLists' in data['MRData']['StandingsTable']:
        standings_lists = data['MRData']['StandingsTable']['StandingsLists']
        if standings_lists:
            teams = standings_lists[0].get('ConstructorStandings', [])
            if teams:
                df_teams = pd.json_normalize(teams)
                return df_teams
            else:
                print(f"No team data available for {season}.")
                return pd.DataFrame()  # Return empty DataFrame if no team data
        else:
            print(f"No standings list data available for {season}.")
            return pd.DataFrame()  # Return empty DataFrame if no standings list
    else:
        print(f"Invalid or missing data for {season}.")
        return pd.DataFrame()  # Return empty DataFrame if structure is invalid

# Example: Fetch team data for the 2025 season
df_teams = get_team_data(2024)

# Check if data is available before saving
if not df_teams.empty:
    df_teams.to_csv('data/processed/team_data_2025.csv', index=False)
else:
    print("No team data to save.")
