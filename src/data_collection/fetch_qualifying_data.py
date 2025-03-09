import requests
import pandas as pd

# List of 2025 drivers
current_drivers = [
    "Pierre Gasly", "Jack Doohan", "Lance Stroll", "Fernando Alonso",
    "Charles Leclerc", "Lewis Hamilton", "Esteban Ocon", "Oliver Bearman",
    "Nico Hulkenberg", "Gabriel Bortoleto", "Oscar Piastri", "Lando Norris",
    "George Russell", "Andrea Kimi Antonelli", "Isack Hadjar", "Yuki Tsunoda",
    "Max Verstappen", "Liam Lawson", "Alexander Albon", "Carlos Sainz"
]

def fetch_qualifying_results(year):
    url = f"http://ergast.com/api/f1/{year}/qualifying.json?limit=500"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to fetch qualifying data for {year}")
        return None
    
    try:
        data = response.json()
        races = data['MRData']['RaceTable']['Races']
        qualifying_results = []
        
        for race in races:
            race_name = race['raceName']
            circuit = race['Circuit']['circuitName']
            round_num = race['round']
            date = race['date']
            
            for result in race['QualifyingResults']:
                driver = result['Driver']['familyName']
                full_name = f"{result['Driver']['givenName']} {driver}"
                
                # Only include drivers from the 2025 grid
                if full_name in current_drivers:
                    qualifying_position = result['position']
                    team = result['Constructor']['name']
                    
                    qualifying_results.append([year, round_num, date, race_name, circuit, full_name, team, qualifying_position])
        
        return qualifying_results
    
    except requests.exceptions.JSONDecodeError:
        print(f"Error decoding JSON for {year}. The response may be empty or malformed.")
        return None

# Example usage:
year = 2024  # Specify the year you're interested in
qualifying_results = fetch_qualifying_results(year)

if qualifying_results:
    df = pd.DataFrame(qualifying_results, columns=['Year', 'Round', 'Date', 'Race Name', 'Circuit', 'Driver', 'Team', 'Qualifying Position'])
    df.to_csv(f"data/processed/qualifying_results_{year}.csv", index=False)
    print(f"Qualifying results for {year} saved successfully.")
