from . import db

class properties_info(db.Model):
    __tablename__ = 'properties_info'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    bedroom = db.Column(db.Numeric(1000, 1))
    bathroom = db.Column(db.Numeric(1000, 1))
    location = db.Column(db.String(255))
    price = db.Column(db.Numeric(1000, 2))
    description = db.Column(db.String(500))
    type = db.Column(db.String(10))
    photo = db.Column(db.String(500))

    def __init__(self, title, bedroom, bathroom, location, price, description, type, photo):
        self.title = title
        self.bedroom = bedroom
        self.bathroom = bathroom
        self.location = location
        self.price = price
        self.description = description
        self.type = type
        self.photo = photo