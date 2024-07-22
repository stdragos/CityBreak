from flask import *
from flask_restful import Api
import models.Database as Database
from resources.EventResource import EventResource
import os

event_app = Flask('events')

db_host = os.environ.get('DB_HOST') or 'localhost'
db_user = os.environ.get('DB_USER') or 'myuser'
db_pw = os.environ.get('DB_PASSWORD') or 'mypassword'

db_url = f'mysql://{db_user}:{db_pw}@{db_host}/citybreak'

event_app.config['SQLALCHEMY_DATABASE_URI'] = db_url
api = Api(event_app)

db = Database.db
db.init_app(event_app)

with event_app.app_context():
    db.create_all()

api.add_resource(EventResource, '/event')

if __name__ == '__main__':
    event_app.run(host='0.0.0.0', port=5002, debug=True)
