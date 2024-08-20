from flask import *
from flask_restful import Api
from EventAPI import EventAPI
from WeatherAPI import WeatherAPI
import os

gateway_app = Flask('Citybreak')
api = Api(gateway_app)

PORT = os.environ.get('PORT', 5000)
HOST = os.environ.get('HOST', '0.0.0.0')

@gateway_app.route('/')
def index():
    return '''
    <html> <body> <strong> <h1>
    Welcome to CityBreak!

    </h1> </strong> </body> </html>
    '''


api.add_resource(EventAPI, '/event')
api.add_resource(WeatherAPI, '/weather')


if __name__ == '__main__':
    gateway_app.run(host=HOST, port=PORT, debug=True)
