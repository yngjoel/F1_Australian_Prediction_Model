import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Get the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

def get_data_path(filename):
    return os.path.abspath(os.path.join(script_dir, "..", "..", "data", "processed", filename))

# Load processed data
lap_records = pd.read_csv(get_data_path("processed_lap_records.csv"))
circuit_data = pd.read_csv(get_data_path("processed_circuit_data.csv"))
race_results = pd.read_csv(get_data_path("processed_race_results.csv"))
weather_data = pd.read_csv(get_data_path("processed_weather_data.csv"))


# Convert lap time to numeric if necessary
if "Lap Time" in lap_records.columns:
    lap_records["Lap Time (s)"] = pd.to_numeric(lap_records["Lap Time (s)"], errors="coerce")



# Check for missing values
print("Missing Values:\n")
print("Lap Records:", lap_records.isnull().sum())
print("Circuit Data:", circuit_data.isnull().sum())
print("Race Results:", race_results.isnull().sum())
print("Weather Data:", weather_data.isnull().sum())

# Summary Statistics
print("\nSummary Statistics:")
print(lap_records.describe())

# Correlation Heatmap (drop non-numeric columns)
numeric_lap_records = lap_records.select_dtypes(include=["number"])
plt.figure(figsize=(10,6))
sns.heatmap(numeric_lap_records.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap - Lap Records")
plt.show()

# Lap Time Distribution
plt.figure(figsize=(8,5))
sns.histplot(lap_records["Lap Time (s)"], bins=20, kde=True)
plt.xlabel("Lap Time (seconds)")
plt.ylabel("Frequency")
plt.title("Lap Time Distribution")
plt.show()

# Trend of fastest lap times over years
plt.figure(figsize=(10,5))
sns.regplot(x=lap_records["Year"], y=lap_records["Lap Time (s)"], scatter_kws={'s': 50}, line_kws={'color': 'red'})
plt.xlabel("Year")
plt.ylabel("Fastest Lap Time (seconds)")
plt.title("Fastest Lap Times Over the Years with Trendline")
plt.show()

# Weather impact on race results (if applicable)
if "Temperature" in weather_data.columns:
    plt.figure(figsize=(8,5))
    sns.boxplot(x=weather_data["Temperature"], y=race_results["Position"])
    sns.boxplot(x="Year", y="Lap Time (s)", data=lap_records)
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Race Position")
    plt.title("Impact of Temperature on Race Position")
    plt.show()

print(lap_records.dtypes)

print(lap_records.head())

print("EDA Completed!")
