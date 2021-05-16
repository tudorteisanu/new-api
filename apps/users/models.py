from settings import db
from datetime import datetime as dt


def get_timestamp():
    now = dt.now().timestamp()
    time = str(now).split('.')[0]
    return int(time)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128))
    password_hash = db.Column(db.String(256))
    token = db.Column(db.String)
    old_token = db.Column(db.String)
    name = db.Column(db.String(128))
    role = db.Column(db.String(12), server_default='user')
    platform = db.Column(db.String, server_default='')
    browser = db.Column(db.String, server_default='')
    
    def __repr__(self):
        return 'User {} - {}'.format(self.email, self.id)


validations = {
    "id": 'required,unique',
    "email": 'required,min:15,max:128',
    "name": 'required,min:10,max:100'
}