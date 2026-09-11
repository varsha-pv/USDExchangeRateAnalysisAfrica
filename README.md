# Currency Watch — Set D

## Overview

Currency Watch is a Python-based financial data analysis project for Set D. It analyzes exchange-rate data for South Africa, Egypt, Nigeria, and Kenya.

The project covers data cleaning, rolling-window analysis, visualization, interactive mapping, a Streamlit dashboard, and a bonus analysis combining currency data with inflation and GDP growth.

## Objectives

- Clean and prepare currency exchange-rate data.
- Analyze short-term and long-term currency movements.
- Calculate rolling volatility.
- Identify currency volatility and major movements.
- Visualize currency trends.
- Compare currency performance.
- Create an interactive geographical currency map.
- Build an interactive Streamlit dashboard.
- Combine currency performance with inflation and GDP growth.
- Analyze correlations between economic indicators and currency performance.

## Datasets

### Currency Dataset

File:

`day2_currency_setD.csv`

Columns:

- `date` — Date of observation
- `pair` — Currency pair
- `open` — Opening exchange rate
- `high` — Highest exchange rate
- `low` — Lowest exchange rate
- `close` — Closing exchange rate

Currencies analyzed:

- USD/KES — Kenyan Shilling
- USD/NGN — Nigerian Naira
- USD/ZAR — South African Rand
- USD/EGP — Egyptian Pound

### World Bank Dataset

File:

`day2_wb_setD(1).csv`

Columns:

- `country` — Country name
- `year` — Year
- `inflation_pct` — Inflation percentage
- `gdp_growth_pct` — GDP growth percentage

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Plotly
- Streamlit
- Folium
- Streamlit-Folium

## Project Structure

```text
HACK2/
│
├── app.py
│
├── task1_cleaning_setD.py
├── task2_rolling_setD.py
├── task3_visualization_setD.py
│
├── bonus_setD.py
├── bonus_visualization.py
├── bonus_summary.py
│
├── day2_currency_setD.csv
├── day2_wb_setD(1).csv
├── cleaned_setD.csv
│
├── setD_task2_rolling_results.csv
├── setD_task2_long_term_trend.csv
├── setD_task2_direction.csv
├── setD_task2_summary.csv
│
├── setD_trend_chart.png
├── setD_volatility_chart.png
├── setD_currency_map.html
├── setD_map_summary.csv
│
├── bonus_cleaned_worldbank.csv
├── bonus_cleaned_currency.csv
├── bonus_yearly_currency.csv
├── bonus_merged_analysis.csv
├── bonus_correlation_matrix.csv
├── bonus_country_summary.csv
│
├── bonus_inflation_vs_currency.png
├── bonus_gdp_vs_currency.png
├── bonus_inflation_vs_volatility.png
└── bonus_gdp_vs_volatility.png