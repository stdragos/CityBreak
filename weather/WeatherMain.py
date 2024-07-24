import weather.databases.WeatherDatabase as Database
from weather.resources.WeatherResource import WeatherResource
from flask import *
from flask_restful import Api

import os

weather_app = Flask('weather')

db_host = os.environ.get('DB_HOST') or 'localhost'
db_user = os.environ.get('DB_USER') or 'myuser'
db_pw = os.environ.get('DB_PASSWORD') or 'mypassword'

db_url = f'mysql://{db_user}:{db_pw}@{db_host}/citybreak'

weather_app.config['SQLALCHEMY_DATABASE_URI'] = db_url
api = Api(weather_app)

db = Database.db
db.init_app(weather_app)

with weather_app.app_context():
    db.create_all()

api.add_resource(WeatherResource, '/weather')

if __name__ == '__main__':
    weather_app.run(host='0.0.0.0', port=5001, debug=True)
