from settings import db


class Center(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer, nullable=False, default=0)
    weight = db.Column(db.Float, nullable=False, default="")
    name = db.Column(db.String, default="")
    symbol = db.Column(db.String, default="")
    
    def __repr__(self):
        return f'Center {self.name} {self.id}'
