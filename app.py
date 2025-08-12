from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Registered Blueprints
from routes.datafetch import weather_bp, prediction_bp, soil_values_bp
app.register_blueprint(weather_bp)
app.register_blueprint(prediction_bp)
app.register_blueprint(soil_values_bp)


if __name__ == '__main__':
    app.run(debug=True)
