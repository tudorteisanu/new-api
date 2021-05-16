from settings import db


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String, default="")
    name = db.Column(db.String, default="")
    guard = db.Column(db.String, default="")
    
    def __repr__(self):
        return 'Role {} - {}'.format(self.name, self.id)


class Validation:
    validators = {
        "alias": 'required,str,min:3,max:100',
        "name": 'required,min:3,max:100',
        "guard": 'required,str,min:3,max:100'
    }