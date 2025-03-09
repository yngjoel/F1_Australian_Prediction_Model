import requests
import pandas as pd

# Function to get all drivers for a given season
def get_all_drivers(season):
    url = f'http://ergast.com/api/f1/{season}/drivers.json'
    response = requests.get(url)
    data = response.json()

    # Extract all drivers' information
    if 'MRData' in data and 'DriverTable' in data['MRData'] and 'Drivers' in data['MRData']['DriverTable']:
        drivers = data['MRData']['DriverTable']['Drivers']
        driver_ids = [driver['driverId'] for driver in drivers]  # Extract driver IDs
        return driver_ids
    else:
        print(f"No driver data available for season {season}.")
        return []

# Function to get driver race history data
def get_driver_history_data(driver_id, season):
    url = f'http://ergast.com/api/f1/{season}/drivers/{driver_id}/results.json'
    response = requests.get(url)
    data = response.json()

    # Extract driver results data
    if 'MRData' in data and 'RaceTable' in data['MRData'] and 'Races' in data['MRData']['RaceTable']:
        results = data['MRData']['RaceTable']['Races']
        df_results = pd.json_normalize(results)
        return df_results
    else:
        print(f"No race data available for driver {driver_id} in season {season}.")
        return pd.DataFrame()  # Return an empty DataFrame if no data

# Main script to get all drivers' data for a season
def get_all_driver_data(season):
    driver_ids = get_all_drivers(season)
    all_driver_data = pd.DataFrame()  # Empty DataFrame to store all driver data

    for driver_id in driver_ids:
        print(f"Fetching data for driver {driver_id}...")
        driver_data = get_driver_history_data(driver_id, season)
        
        if not driver_data.empty:
            driver_data['Driver_ID'] = driver_id  # Add driver ID as a column for identification
            all_driver_data = pd.concat([all_driver_data, driver_data], ignore_index=True)
    
    # Save the complete data to a CSV file
    if not all_driver_data.empty:
        all_driver_data.to_csv(f'data/processed/driver_history_{season}.csv', index=False)
        print(f"Data saved to driver_history_{season}.csv")
    else:
        print("No driver data to save.")

# Example: Fetch data for all drivers for the 2024 season
get_all_driver_data(2024)
