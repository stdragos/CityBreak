from flask import *
from sqlalchemy import *
from dateutil.parser import parse
from datetime import date as ddate, datetime
import models.Database as Database
from models.Weather import Weather

db = Database.db


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
        elif len(city) > 50:
            return f'City must be less than 50 characters', 404
        elif date is None:
            return f'You must insert a date', 404
        elif temperature is None:
            return f'You must insert a temperature', 404
        elif humidity is None or float(humidity) < 0:
            return f'You must insert a humidity', 404
        elif description is None:
            return f'You must insert a description', 404
        elif len(description) > 50:
            return f'Description must be less than 50 characters', 404
        else:
            try:
                res = bool(datetime.strptime(date, "%Y-%m-%d"))
                if res is False:
                    raise ValueError
            except ValueError:
                return f'Invalid date', 404

        return true, 201