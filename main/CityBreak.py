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


def run_app(application, port):
    application.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)


if __name__ == '__main__':
    gateway_app.run(host='0.0.0.0', port=5000, debug=True)

    # weather_thread = Thread(target=run_app, args=(weatherResource.app, 5001,))
    # event_thread = Thread(target=run_app, args=(eventResource.app, 5002,))
    #
    # weather_thread.start()
    # event_thread.start()
    #
    #
    # weather_thread.join()
    # event_thread.join()
