from settings import db
from sqlalchemy.dialects.postgresql import JSONB

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, default='')
