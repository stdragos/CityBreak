from flask import *
from flask_restful import Api
from EventDatabase import db
from EventResource import EventResource
import os
event_app = Flask('events')

PORT = os.environ.get('PORT', 5002)
HOST = os.environ.get('HOST', '0.0.0.0')

db_host = os.environ.get('DB_HOST') or '127.0.0.1'
db_user = os.environ.get('DB_USER') or 'myuser'
db_pw = os.environ.get('DB_PASSWORD') or 'mypassword'

db_url = f'mysql://{db_user}:{db_pw}@{db_host}/event'

event_app.config['SQLALCHEMY_DATABASE_URI'] = db_url
api = Api(event_app)

db.init_app(event_app)

with event_app.app_context():
    db.create_all()

api.add_resource(EventResource, '/event')

if __name__ == '__main__':
    event_app.run(host=HOST, port=PORT, debug=True)
