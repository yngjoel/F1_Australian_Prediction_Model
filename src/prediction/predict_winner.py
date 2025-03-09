import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Load Data
df_results = pd.read_csv('data/processed/filtered_f1_results.csv')  # Updated dataset
df_weather = pd.read_csv('data/processed/processed_weather_data.csv')
df_lap = pd.read_csv('data/processed/processed_lap_records.csv')

# Merge datasets
merged_df = df_results.merge(df_weather, on='Year', how='left')
merged_df = merged_df.merge(df_lap[['Year', 'Lap Time (s)']], on='Year', how='left')

# Drop rows with missing values
merged_df.dropna(inplace=True)

# Ensure 'Winner' column exists
merged_df['Winner'] = merged_df.loc[merged_df['Position'] == 1, 'Driver']
merged_df['Winner'].fillna(method='ffill', inplace=True)  # Fill missing values

# Encode 'Winner'
le_winner = LabelEncoder()
merged_df['Winner'] = le_winner.fit_transform(merged_df['Winner'])


le_team = LabelEncoder()
merged_df['Team'] = le_team.fit_transform(merged_df['Team'])

# Select features and target
X = merged_df[['Temp_C', 'Precip_mm', 'Wind_kmh', 'Pressure_hPa', 'Lap Time (s)', 'Team']]
y = merged_df['Winner']

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train Logistic Regression
log_model = LogisticRegression(max_iter=500)
log_model.fit(X_train, y_train)
y_pred_log = log_model.predict(X_test)
log_accuracy = accuracy_score(y_test, y_pred_log)

# Train Random Forest
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)
rf_accuracy = accuracy_score(y_test, y_pred_rf)

# Compare results
print("Logistic Regression Accuracy:", log_accuracy)
print("Random Forest Accuracy:", rf_accuracy)
print("\nRandom Forest Classification Report:\n", classification_report(y_test, y_pred_rf))

# Predict 2025 Winner using 2024 data
latest_data = merged_df[(merged_df['Year'] == 2024) & (merged_df['Round'] == 3)][['Temp_C', 'Precip_mm', 'Wind_kmh', 'Pressure_hPa', 'Lap Time (s)', 'Team']]
latest_data_scaled = scaler.transform(latest_data)

predicted_winner_index = rf_model.predict(latest_data_scaled)[0]
predicted_winner = le_winner.inverse_transform([predicted_winner_index])[0]

print("🏆 Predicted Winner for 2025 Australian GP:", predicted_winner)
