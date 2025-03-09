import pandas as pd
import os

def convert_lap_time_to_seconds(lap_time):
    """Convert lap time from mm:ss.sss format to total seconds."""
    minutes, seconds = lap_time.split(':')
    return float(minutes) * 60 + float(seconds)

def ensure_directory_exists(directory):
    """Ensure that the given directory exists, create if necessary."""
    if not os.path.exists(directory):
        os.makedirs(directory)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_DIR = os.path.join(BASE_DIR, "..", "..", "data", "raw")
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "..", "..", "data", "processed")

def process_lap_records():
    """Load and process lap records data."""
    file_path = os.path.join(RAW_DATA_DIR, "lap_records.csv")
    output_path = os.path.join(PROCESSED_DATA_DIR, "processed_lap_records.csv")
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    ensure_directory_exists(PROCESSED_DATA_DIR)
    
    lap_df = pd.read_csv(file_path)
    lap_df["Lap Time (s)"] = lap_df["Lap Time"].apply(convert_lap_time_to_seconds)
    lap_df.to_csv(output_path, index=False)
    print("Lap records processed and saved.")

def process_circuit_data():
    """Load and clean circuit data."""
    file_path = os.path.join(RAW_DATA_DIR, "circuit_data.csv")
    output_path = os.path.join(PROCESSED_DATA_DIR, "processed_circuit_data.csv")
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    ensure_directory_exists(PROCESSED_DATA_DIR)
    
    circuit_df = pd.read_csv(file_path)
    circuit_df.dropna(inplace=True)
    circuit_df.to_csv(output_path, index=False)
    print("Circuit data processed and saved.")

def process_race_results():
    """Load and clean race results data."""
    file_path = os.path.join(RAW_DATA_DIR, "race_results.csv")
    output_path = os.path.join(PROCESSED_DATA_DIR, "processed_race_results.csv")
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    ensure_directory_exists(PROCESSED_DATA_DIR)
    
    results_df = pd.read_csv(file_path)
    results_df.dropna(inplace=True)
    results_df.to_csv(output_path, index=False)
    print("Race results processed and saved.")

def process_weather_data():
    """Load and clean weather data."""
    file_path = os.path.join(RAW_DATA_DIR, "weather_data.csv")
    output_path = os.path.join(PROCESSED_DATA_DIR, "processed_weather_data.csv")
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    ensure_directory_exists(PROCESSED_DATA_DIR)
    
    weather_df = pd.read_csv(file_path)
    weather_df.dropna(inplace=True)
    weather_df.to_csv(output_path, index=False)
    print("Weather data processed and saved.")

def preprocess_all_data():
    """Run all preprocessing functions."""
    process_lap_records()
    process_circuit_data()
    process_race_results()
    process_weather_data()
    print("All datasets processed successfully.")

if __name__ == "__main__":
    preprocess_all_data()
