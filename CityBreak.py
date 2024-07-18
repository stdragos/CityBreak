import json

import sqlalchemy
from flask import *
from sqlalchemy import *
from flask_restful import Resource
from dateutil.parser import parse
from datetime import date as ddate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

import os

app = Flask('Citybreak')

db_host = os.environ.get('DB_HOST') or 'localhost'
db_user = os.environ.get('DB_USER') or 'myuser'
db_pw = os.environ.get('DB_PASSWORD') or 'mypassword'

db_url = f'mysql://{db_user}:{db_pw}@{db_host}/citybreak'

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
db = SQLAlchemy(app)
api = Api(app)


@app.route('/')
def index():
    return '''
    <html> <body> <strong> <h1>
    Welcome to CityBreak!

    </h1> </strong> </body> </html>
    '''


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50))
    date = db.Column(db.Date)
    title = db.Column(db.String(50))
    description = db.Column(db.String(50))
    active = db.Column(db.Boolean)

    def to_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Events(Resource):
    def get(self):
        print(db.session)
        city = request.args.get('city')
        date = request.args.get('date')
        title = request.args.get('title')
        date_filter = request.args.get('date_filter')

        if date_filter != 'past' and date_filter != 'future':
            date_filter = None

        return eventService.get(city, date, title, date_filter)

    def post(self):
        city = request.args.get('city')
        date = request.args.get('date')
        title = request.args.get('title')
        description = request.args.get('description')

        print(city)
        event = Event(city=city, date=date, title=title, description=description, active=True)
        db.session.add(event)
        db.session.commit()

        return json.dumps(event), 201

    def put(self):
        id = request.args.get('id')
        city = request.args.get('city')
        date = request.args.get('date')
        title = request.args.get('title')
        description = request.args.get('description')

        if id is None:
            return f'You must insert an ID', 404

        res = eventService.check_fields(city, date, title, description)

        if res[1] == 201:

            obj_to_edit = db.session.query(Event).filter(Event.id == id).all()
            if obj_to_edit:
                obj_to_edit[0].city = city if city else obj_to_edit[0].city
                obj_to_edit[0].date = date if date else obj_to_edit[0].date
                obj_to_edit[0].title = title if title else obj_to_edit[0].title
                obj_to_edit[0].description = description if description else obj_to_edit[0].description

                db.session.add(obj_to_edit[0])
                db.session.commit()

                return "OK", 201

            else:
                return f'Invalid id', 404

        else:
            return res[0], res[1]

    def delete(self):
        id = request.args.get('id')
        if id:
            obj_to_edit = db.session.query(Event).filter(Event.id == id).all()

            if obj_to_edit:
                obj_to_edit[0].active = False
                db.session.add(obj_to_edit[0])
                db.session.commit()
                return "OK", 201
            else:
                return f'Invalid id', 404


class EventService:
    def get(self, city, date, title, date_filter):
        return json.jsonify(
            [p.to_dict() for p in
             db.session.query(Event).filter(and_(Event.active == True, or_(Event.city == city, city is None),
                                                 or_(Event.date == date, date is None),
                                                 or_(Event.title == title, title is None),
                                                 or_(date_filter is None,
                                                     date_filter == 'past' and Event.date < ddate.today(),
                                                     date_filter == 'future' and Event.date > ddate.today()))).all()])

    def check_fields(self, city, date, title, description):
        if not city:
            return f'Missing value for city', 404
        elif not date:
            return f'Missing value for date', 404
        elif not title:
            return f'Missing value for title', 404
        elif not description:
            return f'Missing value for description', 404
        else:
            try:
                parse(date)
            except ValueError:
                return f'Invalid date', 404

        return true, 201


class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50))
    date = db.Column(db.Date)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    description = db.Column(db.String(50))
    active = db.Column(db.Boolean)

    def to_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Weathers(Resource):
    def get(self):
        print(db.session)
        city = request.args.get('city')
        date = request.args.get('date')
        celsius = request.args.get('celsius')

        if celsius is None:
            celsius = "true"
        else:
            celsius = celsius.lower()

        return weatherService.get(city=city, date=date, celsius=celsius)

    def post(self):
        city = request.args.get('city')
        date = request.args.get('date')
        temperature = request.args.get('temperature')
        humidity = request.args.get('humidity')
        description = request.args.get('description')

        weather = Weather(city=city, date=date, temperature=temperature, humidity=humidity, description=description,
                          active=True)
        db.session.add(weather)
        db.session.commit()

        print(weather.to_dict())

        return weather.to_dict(), 201

    def put(self):
        id = request.args.get('id')
        city = request.args.get('city')
        date = request.args.get('date')
        temperature = request.args.get('temperature')
        humidity = request.args.get('humidity')
        description = request.args.get('description')

        if id is None:
            return f'You must insert an ID', 404

        res = weatherService.check_fields(city, date, temperature, humidity, description)

        if res[1] == 201:

            obj_to_edit = db.session.query(Weather).filter(Weather.id == id).all()
            if obj_to_edit:
                obj_to_edit[0].city = city if city else obj_to_edit[0].city
                obj_to_edit[0].date = date if date else obj_to_edit[0].date
                obj_to_edit[0].temperature = temperature if temperature else obj_to_edit[0].temperature
                obj_to_edit[0].humidity = humidity if humidity else obj_to_edit[0].humidity
                obj_to_edit[0].description = description if description else obj_to_edit[0].description

                db.session.add(obj_to_edit[0])
                db.session.commit()

                return "OK", 201

            else:
                return f'Invalid id', 404

        else:
            return res[0], res[1]

    def delete(self):
        id = request.args.get('id')
        if id:
            obj_to_edit = db.session.query(Weather).filter(Weather.id == id).all()

            if obj_to_edit:
                obj_to_edit[0].active = False
                db.session.add(obj_to_edit[0])
                db.session.commit()
                return "OK", 201
            else:
                return f'Invalid id', 404


class WeatherService:
    def get(self, city, date, celsius):
        objects = [p.to_dict() for p in db.session.query(Weather).filter(
            and_(Weather.active == True,
                 or_(Weather.city == city, city is None),
                 or_(Weather.date == date, date is None))).all()]

        if celsius == 'false':
            for obj in objects:
                if obj['temperature']:
                    obj['temperature'] = obj['temperature'] * 9 / 5 + 32

        return json.jsonify(objects)

    def check_fields(self, city, date, temperature, humidity, description):
        if city is None:
            return f'You must insert a city', 404
        elif date is None:
            return f'You must insert a date', 404
        elif temperature is None:
            return f'You must insert a temperature', 404
        elif humidity is None or float(humidity) < 0:
            return f'You must insert a humidity', 404
        elif description is None:
            return f'You must insert a description', 404
        else:
            try:
                parse(date)
            except ValueError:
                return f'Invalid date', 404

        return true, 201


api.add_resource(Events, '/event')
api.add_resource(Weathers, '/weather')

eventService = EventService()
weatherService = WeatherService()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
