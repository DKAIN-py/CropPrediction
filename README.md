# CropPrediction

CropPrediction is a Flask-based web application that recommends the best crops to plant in a given location in India by analyzing real-time weather and soil data. The system uses a trained Yggdrasil Decision Forests model to generate location-specific recommendations.

## Overview

The application is intended to help farmers, agricultural planners, and researchers make data-driven decisions. It retrieves weather and soil parameters for your coordinates and predicts the most suitable crops for that region.

## Features

- Real-time weather data retrieval for any location in India
- Soil parameter fetching from Indian datasets
- Machine learning-based crop recommendation using Yggdrasil Decision Forests
- Modular Flask Blueprint structure
- Lightweight and fast

## Installation

### Clone the repository
```bash
git clone https://github.com/DKAIN-py/CropPrediction.git
cd CropPrediction
````

### Create and activate virtual environment

```bash
python3 -m venv .venv
```

#### Linux/macOS

```bash
source .venv/bin/activate
```

#### Windows

```bash
.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

```bash
python app.py
```

Server will start at `localhost:5000`

## Notes

* Currently supported in India only
* Requires Internet access
* Still in Development phase

```
