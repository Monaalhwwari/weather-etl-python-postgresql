# Weather ETL Pipeline (Python & PostgreSQL)

This project is an end-to-end ETL pipeline that extracts real-time weather data from an API, transforms and cleans the data using Pandas, and loads it into a PostgreSQL database.

## Features
- Extracts real-time weather data from the Open-Meteo API
- Cleans and transforms raw data (handling missing values, formatting, and calculations)
- Loads structured data into PostgreSQL using SQLAlchemy

## ETL Process

### 1. Extract
- Sends a request to the API to retrieve weather data in JSON format  
- Implements error handling using try/except  
- Returns the response if successful, otherwise handles errors gracefully  

### 2. Transform
- Parses JSON data into a data frame structure using Pandas  
- Cleans the dataset (handles missing values)  
- Performs basic analysis (calculating average daily temperature)  

### 3. Load
- Loads the processed data directly into PostgreSQL  
- Uses SQLAlchemy for efficient database interaction and to load data into postgreSQL 

## Technologies Used
- Python
- Pandas
- SQLAlchemy
- PostgreSQL
- Open-Meteo API
