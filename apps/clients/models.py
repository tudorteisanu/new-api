from settings import db


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, default="")
    name = db.Column(db.String, default="")
    
    def __repr__(self):
        return 'Client {} - {}'.format(self.name, self.id)


