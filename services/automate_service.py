from flask import jsonify
import openmeteo_requests
from retry_requests import retry
import requests_cache
import numpy as np
from datetime import datetime, timedelta
import geopandas as gpd
from shapely.geometry import Point
import pandas as pd


# error class
class DistrictNotFoundError(Exception):
    """Raised when the district could not be determined from coordinates."""
    pass


# Open-Meteo setup
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)


def fetch_weather(lat,lon):
    print(f"{lat}, {lon}")
    if lat is None or lon is None:
        return jsonify({"error": "lat and lon are required"}), 400

    # Get current and 30-day-old dates
    today = datetime.now().date()
    thirty_days_ago = today - timedelta(days=30)

    # Format dates as YYYY-MM-DD
    start_date = thirty_days_ago.strftime('%Y-%m-%d')
    end_date = today.strftime('%Y-%m-%d')

    # Setup API call
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": [
            "temperature_2m",
            "rain",
            "precipitation",
            "relative_humidity_2m"
        ],
        "start_date": start_date,
        "end_date": end_date
    }

    try:
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]

        hourly = response.Hourly()
        temp = hourly.Variables(0).ValuesAsNumpy()
        rain = hourly.Variables(1).ValuesAsNumpy()
        precip = hourly.Variables(2).ValuesAsNumpy()
        humidity = hourly.Variables(3).ValuesAsNumpy()

        avg_temp = float(np.nanmean(temp))
        avg_humidity = float(np.nanmean(humidity))
        total_rainfall = float(np.nansum(precip))  # mm

        return jsonify({
            "avg_temperature": round(avg_temp, 2),
            "avg_humidity": round(avg_humidity, 2),
            "total_rainfall": round(total_rainfall, 2)
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to fetch weather data"}), 500
    


def get_district_from_latlon(lat, lon):
    # Load the unzipped GeoJSON file
    gdf = gpd.read_file("dataFiles/gadm41_IND_2.json")

    # Example point (lon, lat — note the order)
    point = Point(lon, lat)

    # Find the matching district polygon
    match = gdf[gdf.contains(point)]

    district = match.iloc[0]["NAME_2"]  # district name
    state = match.iloc[0]["NAME_1"]     # state name
        
    district = (str(district)).upper()

    soil_df = pd.read_csv("dataFiles/combined_soil_data.csv")

    dist_list = soil_df["District"].unique()

    try:
        if district not in dist_list:
            raise DistrictNotFoundError("Data of your place is not present right now")
        i = 0
        for dist in dist_list:
            if district==dist:
                data = {
                        "N": soil_df["N"][i],
                        "P": soil_df["P"][i],
                        "K": soil_df["K"][i],
                        "pH": soil_df["pH"][i]
                        }
                return jsonify(data)
            i+=1

    except DistrictNotFoundError as e:
        print(e)
        return jsonify({"error":"Could not find the data for this place"})
         






