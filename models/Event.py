import models.Database as Database

db = Database.db


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50))
    date = db.Column(db.Date)
    title = db.Column(db.String(50))
    description = db.Column(db.String(50))
    price = db.Column(db.Float)
    location = db.Column(db.String(50))
    active = db.Column(db.Boolean)

    def to_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
