import requests
from flask import *
from flask_restful import Api
import models.Database as Database
from resources.WeatherResource import WeatherResource
import resources.WeatherResource as weatherResource
from flask_restful import Resource

WEATHER_URL = 'http://127.0.0.1:5001/weather'


class WeatherAPI(Resource):
    def get(self):
        response = requests.get(WEATHER_URL, params=request.args)
        return response.json(), response.status_code

    def put(self):
        response = requests.put(WEATHER_URL, params=request.args)
        return response.json(), response.status_code

    def post(self):
        response = requests.post(WEATHER_URL, params=request.args)
        return response.json(), response.status_code

    def delete(self):
        response = requests.delete(WEATHER_URL, params=request.args)
        return response.json(), response.status_code
