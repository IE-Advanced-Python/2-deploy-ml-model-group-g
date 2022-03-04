from flask import Flask, request
from ie_bike_model import ai
import ie_bike_model
import sys
import time
import sklearn

app = Flask(__name__)

@app.route("/")
def hello():

    return {
        "Scikit version:": sklearn.__version__,
        "Python version:": ".".join(map(str, sys.version_info)),
        "ie_bike_model": ie_bike_model.__version__,
    }


@app.route("/predict")
def predict():
    weather_dict = {
    "clear": "Clear, Few clouds, Partly cloudy, Partly cloudy",
    "cloudy": "Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist",
    "light_rain":"Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds",
    "heavy_rain":"Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog"
    }

    start_time = time.time()

    dteday = request.args.get("date")
    hr = int(request.args.get("hour"))
    weathersit = weather_dict[request.args.get("weather_situation")]
    temp = float(request.args.get("temperature"))
    atemp = float(request.args.get("feeling_temperature"))
    hum = float(request.args.get("humidity"))
    windspeed = float(request.args.get("windspeed"))
    result = ai.predict(
        dteday=dteday,
        hr=hr,
        weathersit=weathersit,
        temp=temp,
        atemp=atemp,
        hum=hum,
        windspeed=windspeed,
    )
    return {"result": result, "elapsed_fime": (time.time() - start_time)}


@app.route("/train_and_persist")
def train_and_persist():
    ai.train_and_persist()
    return {"status": "ok"}


app.run(host="0.0.0.0", port=sys.argv[1])
