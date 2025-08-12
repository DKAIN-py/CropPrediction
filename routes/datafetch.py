from flask import Blueprint, request
from services.automate_service import fetch_weather, get_district_from_latlon
from services.default_service import get_prediction

weather_bp = Blueprint("weather",__name__)
prediction_bp = Blueprint("prediction",__name__)
soil_values_bp = Blueprint("soil_values",__name__)


@weather_bp.route("/get-weather", methods=["POST", "GET"])
def get_weather():
    if request.method == "POST":
        data = request.get_json()
        lat = data.get("lat")
        lon = data.get("lon")
    else:
        # Default values for testing or GET request
        lat = 26.8467
        lon = 80.9462

    weather = fetch_weather(lat, lon)
    return weather




@prediction_bp.route("/",methods=["GET","POST"])
def predict():
    return get_prediction()


@soil_values_bp.route("/soil-values", methods=["POST", "GET"])
def NPK_values():

    data = request.get_json()
    lat = data.get("lat")
    lon = data.get("lon")
    

    return get_district_from_latlon(lat, lon)


