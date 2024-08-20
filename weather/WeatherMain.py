import WeatherDatabase as WeatherDatabase
from WeatherResource import WeatherResource
from flask import *
from flask_restful import Api

import os

PORT = os.environ.get('PORT', 5001)
HOST = os.environ.get('HOST', '0.0.0.0')

weather_app = Flask('weather')

db_host = os.environ.get('DB_HOST') or '127.0.0.1'
db_user = os.environ.get('DB_USER') or 'myuser'
db_pw = os.environ.get('DB_PASSWORD') or 'mypassword'

db_url = f'mysql://{db_user}:{db_pw}@{db_host}/weather'

weather_app.config['SQLALCHEMY_DATABASE_URI'] = db_url
api = Api(weather_app)

db = WeatherDatabase.db
db.init_app(weather_app)

with weather_app.app_context():
    db.create_all()

api.add_resource(WeatherResource, '/weather')

if __name__ == '__main__':
    weather_app.run(host=HOST, port=PORT, debug=True)
