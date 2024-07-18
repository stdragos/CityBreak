from flask import *
from flask_restful import Api
import models.Database as Database
from resources.WeatherResource import WeatherResource
from resources.EventResource import EventResource

import os

app = Flask('Citybreak')

db_host = os.environ.get('DB_HOST') or 'localhost'
db_user = os.environ.get('DB_USER') or 'myuser'
db_pw = os.environ.get('DB_PASSWORD') or 'mypassword'

db_url = f'mysql://{db_user}:{db_pw}@{db_host}/citybreak'

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
api = Api(app)

db = Database.db
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return '''
    <html> <body> <strong> <h1>
    Welcome to CityBreak!

    </h1> </strong> </body> </html>
    '''


api.add_resource(EventResource, '/event')
api.add_resource(WeatherResource, '/weather')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
