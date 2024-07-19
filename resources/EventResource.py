from flask import *
from flask_restful import Api
import models.Database as Database
from services.EventService import EventService
from models.Event import Event
from flask_restful import Resource

import os

app = Flask('events')

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

eventService = EventService()


class EventResource(Resource):
    def get(self):
        city = request.args.get('city')
        date = request.args.get('date')
        title = request.args.get('title')
        date_filter = request.args.get('date_filter')
        price = request.args.get('price')
        location = request.args.get('location')

        if date_filter != 'past' and date_filter != 'future':
            date_filter = None

        return eventService.get(city, date, title, date_filter, price, location)

    def post(self):
        city = request.args.get('city')
        date = request.args.get('date')
        title = request.args.get('title')
        description = request.args.get('description')
        price = request.args.get('price')
        location = request.args.get('location')

        res = eventService.check_fields(city, date, title, description, price, location)
        if res[1] == 201:
            event = Event(city=city, date=date, title=title, description=description, price=price, location=location, active=True)
            db.session.add(event)
            db.session.commit()

            return event.to_dict(), 201

        else:
            return res[0], res[1]

    def put(self):
        id = request.args.get('id')
        city = request.args.get('city')
        date = request.args.get('date')
        title = request.args.get('title')
        price = request.args.get('price')
        location = request.args.get('location')
        description = request.args.get('description')

        if id is None:
            return f'You must insert an ID', 404

        res = eventService.check_fields(city, date, title, description, price, location)

        if res[1] == 201:

            obj_to_edit = db.session.query(Event).filter(Event.id == id).all()
            if obj_to_edit:
                obj_to_edit[0].city = city if city else obj_to_edit[0].city
                obj_to_edit[0].date = date if date else obj_to_edit[0].date
                obj_to_edit[0].title = title if title else obj_to_edit[0].title
                obj_to_edit[0].description = description if description else obj_to_edit[0].description

                db.session.add(obj_to_edit[0])
                db.session.commit()

                return obj_to_edit[0].to_dict(), 201

            else:
                return f'Invalid id', 404

        else:
            return res[0], res[1]

    def delete(self):
        id = request.args.get('id')
        if id:
            obj_to_edit = db.session.query(Event).filter(Event.id == id).all()

            if obj_to_edit:
                if not obj_to_edit[0].active:
                    return f'Invalid id', 404
                obj_to_edit[0].active = False
                db.session.add(obj_to_edit[0])
                db.session.commit()
                return "OK", 201
            else:
                return f'Invalid id', 404
        else:
            return f'Invalid id', 404


api.add_resource(EventResource, '/event')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
