# F1 Prediction Model

This repository contains a machine learning model to predict the winner of the Formula 1 Australian Grand Prix (2025) based on historical data and various factors like weather, qualifying performance, pit stop data, and driver/team performance. The model is built using Random Forest and Logistic Regression classifiers.

## Requirements

To run the script, you'll need to install the following Python libraries:

- **pandas**: For data manipulation and analysis.
- **numpy**: For numerical operations.
- **scikit-learn**: For machine learning models, preprocessing, and evaluation.
- **matplotlib** (optional): For data visualization.

### Install the libraries

Run the following command to install all the required dependencies:

```bash
pip install pandas numpy scikit-learn matplotlib
```

File Structure
- data/processed/filtered_f1_results.csv: Processed results data of previous F1 races.
- data/processed/processed_weather_data.csv: Processed weather data for races.
- data/processed/processed_lap_records.csv: Data regarding lap times for races.
- data/processed/qualifying_results_2024.csv: Data regarding qualifying results for the 2024 season.
- data/processed/driver_history_2024.csv: Historical driver data for the 2024 season.
- data/processed/pit_stop_data_2024_australia.csv: Pit stop data specific to the 2024 Australian Grand Prix.
- data/processed/processed_circuit_data.csv: Data regarding the circuits used in races.
- data/processed/team_data_2024.csv: Team-related data for the 2024 season.

  
## Script Overview

The main script uses the following steps:

1.  **Data Preprocessing**:
    
    -   Merging multiple datasets containing race results, weather data, lap times, pit stops, and qualifying data.
    -   Handling missing values and feature engineering (e.g., rolling average position).
2.  **Model Building**:
    
    -   Logistic Regression and Random Forest classifiers are used to predict the winner.
    -   Hyperparameter tuning is done using GridSearchCV to optimize model performance.
3.  **Prediction**:
    
    -   The models are trained on the 2024 data and used to predict the winner of the 2025 Australian Grand Prix.

  
## How to Run

1.  Clone the repository:
    
    bash
    
    CopyEdit
    
    `git clone https://github.com/yourusername/f1-prediction.git` 
    
2.  Navigate into the repository:
    
    bash
    
    CopyEdit
    
    `cd f1-prediction` 
    
3.  Install the dependencies:
    
    bash
    
    CopyEdit
    
    `pip install pandas numpy scikit-learn matplotlib` 
    
4.  Run the script:
    
    bash
    
    CopyEdit
    
    `python predict_winner_3.0.py` 
    

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

-   This project uses historical F1 data and weather information to make predictions.
-   Special thanks to all the open-source libraries used in this project for their amazing work.

css

CopyEdit

 `This markdown file provides a detailed overview of the repository, installation instructions, script details, and how to run`
