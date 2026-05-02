import requests
import time
import pandas as pd
import logging
from sqlalchemy import create_engine

logging.basicConfig(level=logging.INFO)
params = {
    "latitude": 52.52,
    "longitude": 13.41,
    "hourly": ["temperature_2m", "precipitation", "wind_speed_10m"],
    "forecast_days": 7,
    "timezone": "Europe/Berlin"
}

def extract():
    url = "https://api.open-meteo.com/v1/forecast"
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        print(response.status_code)
        return response
    except Exception as e:
        logging.error(f"Error occurred: {e}")

def transform(response):

    data = response.json()
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    hourly = data["hourly"]

    df = pd.DataFrame({
        "time": hourly["time"],
        "temperature_2m": hourly["temperature_2m"],
        "precipitation": hourly["precipitation"],
        "wind_speed_10m": hourly["wind_speed_10m"],
    })
    df["longitude"] = data["longitude"]
    df["latitude"] = data["latitude"]
    df["timezone"] = data["timezone"]
    df["elevation"] = data["elevation"]
    df["forecast_days"] = params["forecast_days"]

    #cleaning date

    df["time"] = pd.to_datetime(df["time"], errors="coerce")
    df = df.dropna(subset=["time"])
    #cleaning temp

    numeric_columns=["temperature_2m", "precipitation", "wind_speed_10m"]
    for i in numeric_columns:
        df[i]= pd.to_numeric(df[i], errors="coerce")
    df = df.dropna(subset=["time"] + numeric_columns)
    #df cleaning strings

    df["day"]=pd.to_datetime(df["time"]).dt.day_name()
    df["day"]=df["day"].astype("string")
    
    #

    df["hour"] = df["time"].dt.hour
    df["daily_mean"] = df.groupby(df["time"].dt.date)["temperature_2m"].transform("mean")
    df["wind_mean"]=df.groupby(df["time"].dt.date)["wind_speed_10m"].transform("mean")
    df["daily_rain"] = df.groupby(df["time"].dt.date)["precipitation"].transform("mean")
    df["diff"]=df["temperature_2m"]-df["daily_mean"]

    morning_df = df[(df["hour"] >= 6) & (df["hour"] <= 12)]

    print(morning_df[["time","temperature_2m","precipitation","wind_speed_10m","daily_mean","daily_rain","diff"]])
    daily_summary = df.groupby("day").agg({
        "temperature_2m": "mean",
        "wind_speed_10m": "mean",
        "precipitation": "sum"
    })

    print(daily_summary)
    return df

def load(df):
    engine = create_engine("postgresql://postgres:Monalaith12.@localhost/small_etl")
    df.to_sql("weather_data", engine, if_exists="replace", index=False)
def main():

    logging.info("ETL started")
    start = time.time()
    response = extract()
    df = transform(response)
    load(df)
    logging.info("ETL finished")
    end = time.time()
    print("Total time in seconds:", end - start)

if __name__ == "__main__":
    main()

