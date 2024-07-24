from flask import *
from sqlalchemy import *
from datetime import date as ddate, datetime
import event.databases.EventDatabase as Database
from event.models.Event import Event

db = Database.db


class EventService:
    def get(self, city, date, title, date_filter, price, location):
        return json.jsonify(
            [p.to_dict() for p in
             db.session.query(Event).filter(and_(Event.active == True, or_(Event.city == city, city is None),
                                                 or_(Event.date == date, date is None),
                                                 or_(Event.title == title, title is None),
                                                 or_(Event.price == price, price is None),
                                                 or_(Event.location == location, location is None),
                                                 or_(date_filter is None,
                                                     date_filter == 'past' and Event.date < ddate.today(),
                                                     date_filter == 'future' and Event.date > ddate.today()))).all()])

    def check_fields(self, city, date, title, description, price, location):
        if not city:
            return f'Missing value for city', 404
        elif len(city) > 50:
            return f'City must be less than 50 characters', 404
        elif not date:
            return f'Missing value for date', 404
        elif not title:
            return f'Missing value for title', 404
        elif len(title) > 50:
            return f'Title must be less than 50 characters', 404
        elif not description:
            return f'Missing value for description', 404
        elif len(description) > 50:
            return f'Description must be less than 50 characters', 404
        elif not price:
            return f'Missing value for price', 404
        elif not location:
            return f'Missing value for location', 404
        elif len(location) > 50:
            return f'Location must be less than 50 characters', 404
        else:
            try:
                res = bool(datetime.strptime(date, "%Y-%m-%d"))
                if res is False:
                    raise ValueError
            except ValueError:
                return f'Invalid date', 404

        return true, 201