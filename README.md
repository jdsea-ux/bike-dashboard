# Bike Sharing Data Analysis Dashboard
This repository contains the final project for the Data Analysis course. It includes a Jupyter Notebook for exploratory data analysis (EDA) and a Streamlit dashboard for interactive data visualization.

## Project Structure
- `/dashboard`: Contains `dashboard.py` and the cleaned datasets (`main_data.csv`, `day_data.csv`).
- `notebook.ipynb`: The main notebook used for data wrangling, exploratory data analysis, and clustering/binning.
- `README.md`: Project documentation.
- `requirements.txt`: List of required Python packages.

## Setup Environment
If you want to run this project locally, follow these steps (Mac/Linux):

1. **Navigate to the project directory:**
   ```bash
   cd dashboard
2. **Create and activate a virtual environment:**
    python3 -m venv venv
    source venv/bin/activate
3. **Install the required libraries:**
    pip install -r requirements.txt

## Run Streamlit App
streamlit run dashboard.py