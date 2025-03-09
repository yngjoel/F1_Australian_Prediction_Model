import requests
import pandas as pd
import time

# Define the range of seasons to fetch
years = list(range(2018, 2025))
current_drivers = [
    "Pierre Gasly", "Jack Doohan", "Lance Stroll", "Fernando Alonso",
    "Charles Leclerc", "Lewis Hamilton", "Esteban Ocon", "Oliver Bearman",
    "Nico Hulkenberg", "Gabriel Bortoleto", "Oscar Piastri", "Lando Norris",
    "George Russell", "Andrea Kimi Antonelli", "Isack Hadjar", "Yuki Tsunoda",
    "Max Verstappen", "Liam Lawson", "Alexander Albon", "Carlos Sainz"
]

def fetch_race_results(year):
    url = f"http://ergast.com/api/f1/{year}/results.json?limit=500"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch data for {year}")
        return None
    
    data = response.json()
    races = data['MRData']['RaceTable']['Races']
    results = []
    
    for race in races:
        race_name = race['raceName']
        circuit = race['Circuit']['circuitName']
        round_num = race['round']
        date = race['date']
        
        for result in race['Results']:
            driver = result['Driver']['familyName']
            full_name = f"{result['Driver']['givenName']} {driver}"
            if full_name in current_drivers:
                position = result['position']
                team = result['Constructor']['name']
                grid = result['grid']
                status = result['status']
                
                results.append([year, round_num, date, race_name, circuit, full_name, team, position, grid, status])
    
    return results

def main():
    all_results = []
    for year in years:
        print(f"Fetching data for {year}...")
        yearly_results = fetch_race_results(year)
        if yearly_results:
            all_results.extend(yearly_results)
        time.sleep(1)  # Prevent API rate limiting
    
    df = pd.DataFrame(all_results, columns=[
        "Year", "Round", "Date", "Race", "Circuit", "Driver", "Team", "Position", "Grid", "Status"
    ])
    df.to_csv("data/processed/filtered_f1_results.csv", index=False)
    print("✅ Data saved as data/processed/filtered_f1_results.csv")

if __name__ == "__main__":
    main()
