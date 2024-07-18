import models.Database as Database

db = Database.db


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