import requests
from flask import *
from flask_restful import Resource

EVENT_URL = 'http://127.0.0.1:5002/event'


class EventAPI(Resource):
    def get(self):
        response = requests.get(EVENT_URL, params=request.args)
        return response.json(), response.status_code

    def put(self):
        response = requests.put(EVENT_URL, params=request.args)
        return response.json(), response.status_code

    def post(self):
        response = requests.post(EVENT_URL, params=request.args)
        return response.json(), response.status_code

    def delete(self):
        response = requests.delete(EVENT_URL, params=request.args)
        return response.json(), response.status_code
