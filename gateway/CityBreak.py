from threading import Thread
from flask import *
from flask_restful import Api
from services.EventAPI import EventAPI
from services.WeatherAPI import WeatherAPI

gateway_app = Flask('Citybreak')
api = Api(gateway_app)


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
    gateway_app.run(host='0.0.0.0', port=5000, debug=True)
