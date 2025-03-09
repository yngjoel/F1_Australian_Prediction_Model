import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Load Data
df_results = pd.read_csv('data/processed/filtered_f1_results.csv')  # Updated dataset
df_weather = pd.read_csv('data/processed/processed_weather_data.csv')
df_lap = pd.read_csv('data/processed/processed_lap_records.csv')
df_qualifying = pd.read_csv('data/processed/qualifying_results_2024.csv')

# List of 2025 grid drivers
current_drivers = [
    "Pierre Gasly", "Jack Doohan", "Lance Stroll", "Fernando Alonso",
    "Charles Leclerc", "Lewis Hamilton", "Esteban Ocon", "Oliver Bearman",
    "Nico Hulkenberg", "Gabriel Bortoleto", "Oscar Piastri", "Lando Norris",
    "George Russell", "Andrea Kimi Antonelli", "Isack Hadjar", "Yuki Tsunoda",
    "Max Verstappen", "Liam Lawson", "Alexander Albon", "Carlos Sainz"
]

# Merge datasets
merged_df = df_results.merge(df_weather, on='Year', how='left')
merged_df = merged_df.merge(df_lap[['Year', 'Lap Time (s)']], on='Year', how='left')
merged_df = merged_df.merge(df_qualifying[['Year', 'Round', 'Driver', 'Qualifying Position']], 
                             on=['Year', 'Round', 'Driver'], how='left')

# Drop rows with missing values
merged_df.dropna(inplace=True)

# Ensure 'Winner' column exists
merged_df['Winner'] = merged_df.loc[merged_df['Position'] == 1, 'Driver']
merged_df['Winner'].fillna(method='ffill', inplace=True)  # Fill missing values

# Encode 'Winner' and 'Team'
le_winner = LabelEncoder()
merged_df['Winner'] = le_winner.fit_transform(merged_df['Winner'])

le_team = LabelEncoder()
merged_df['Team'] = le_team.fit_transform(merged_df['Team'])

# Feature Engineering

# Calculate rolling average position for the last 5 races (Driver Performance)
merged_df = merged_df.sort_values(by=['Driver', 'Year', 'Round'])
merged_df['Driver_Recent_Performance'] = merged_df.groupby('Driver')['Position'].rolling(window=5, min_periods=1).mean().reset_index(0, drop=True)

# Calculate rolling average position for the last 5 races (Team Performance)
merged_df = merged_df.sort_values(by=['Team', 'Year', 'Round'])
merged_df['Team_Recent_Performance'] = merged_df.groupby('Team')['Position'].rolling(window=5, min_periods=1).mean().reset_index(0, drop=True)

# Select features and target
X = merged_df[['Temp_C', 'Precip_mm', 'Wind_kmh', 'Pressure_hPa', 'Lap Time (s)', 'Team', 'Qualifying Position', 'Driver_Recent_Performance', 'Team_Recent_Performance']]
y = merged_df['Winner']

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Hyperparameter tuning for Logistic Regression using GridSearchCV
log_param_grid = {
    'C': [0.1, 1, 10],  # Regularization strength
    'solver': ['lbfgs', 'liblinear'],  # Optimizer
    'max_iter': [100, 200, 300],  # Maximum iterations
    'class_weight': ['balanced', None]  # Class balancing
}

log_grid_search = GridSearchCV(LogisticRegression(), log_param_grid, cv=5, verbose=1, n_jobs=-1)
log_grid_search.fit(X_train, y_train)

# Best parameters and model
best_log_model = log_grid_search.best_estimator_

# Predict and evaluate Logistic Regression
y_pred_log = best_log_model.predict(X_test)
log_accuracy = accuracy_score(y_test, y_pred_log)
print("Logistic Regression Accuracy:", log_accuracy)
print("\nLogistic Regression Classification Report:\n", classification_report(y_test, y_pred_log))

# Hyperparameter tuning for Random Forest using GridSearchCV
rf_param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'class_weight': ['balanced', None]  # Class weighting
}

rf_grid_search = GridSearchCV(RandomForestClassifier(), rf_param_grid, cv=5, verbose=1, n_jobs=-1)
rf_grid_search.fit(X_train, y_train)

# Best parameters and model
best_rf_model = rf_grid_search.best_estimator_

# Predict and evaluate Random Forest
y_pred_rf = best_rf_model.predict(X_test)
rf_accuracy = accuracy_score(y_test, y_pred_rf)
print("Random Forest Accuracy:", rf_accuracy)
print("\nRandom Forest Classification Report:\n", classification_report(y_test, y_pred_rf))

# Predict 2025 Winner using 2024 data
latest_data = merged_df[(merged_df['Year'] == 2024) & (merged_df['Round'] == 3)][['Temp_C', 'Precip_mm', 'Wind_kmh', 'Pressure_hPa', 'Lap Time (s)', 'Team', 'Qualifying Position', 'Driver_Recent_Performance', 'Team_Recent_Performance']]
latest_data_scaled = scaler.transform(latest_data)

# Predict winner using best models
predicted_winner_log_index = best_log_model.predict(latest_data_scaled)[0]
predicted_winner_log = le_winner.inverse_transform([predicted_winner_log_index])[0]

predicted_winner_rf_index = best_rf_model.predict(latest_data_scaled)[0]
predicted_winner_rf = le_winner.inverse_transform([predicted_winner_rf_index])[0]

print("🏆 Predicted Winner for 2025 Australian GP (Logistic Regression):", predicted_winner_log)
print("🏆 Predicted Winner for 2025 Australian GP (Random Forest):", predicted_winner_rf)
