from flask import *
from flask_restful import Resource
import models.Database as Database
from models.Weather import Weather
from services.WeatherService import WeatherService

db = Database.db
weather_service = WeatherService()


class WeatherResource(Resource):
    def get(self):
        city = request.args.get('city')
        date = request.args.get('date')
        celsius = request.args.get('celsius')

        if celsius is None:
            celsius = "true"
        else:
            celsius = celsius.lower()

        return weather_service.get(city=city, date=date, celsius=celsius)

    def post(self):
        city = request.args.get('city')
        date = request.args.get('date')
        temperature = request.args.get('temperature')
        humidity = request.args.get('humidity')
        description = request.args.get('description')

        res = weather_service.check_fields(city, date, temperature, humidity, description)

        if res[1] == 201:
            weather = Weather(city=city, date=date, temperature=temperature, humidity=humidity, description=description,
                              active=True)
            db.session.add(weather)
            db.session.commit()

            return weather.to_dict(), 201

        else:
            return res[0], res[1]

    def put(self):
        id = request.args.get('id')
        city = request.args.get('city')
        date = request.args.get('date')
        temperature = request.args.get('temperature')
        humidity = request.args.get('humidity')
        description = request.args.get('description')

        if id is None:
            return f'You must insert an ID', 404

        res = weather_service.check_fields(city, date, temperature, humidity, description)

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

                return obj_to_edit[0].to_dict(), 201

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

