from flask import request
from flask import jsonify
from settings import db
from apps.users.models import User
from apps.users.schema import UserSchema


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


class UserRoute(object):
    @staticmethod
    def get_data():
        headers = [
            {"value": "id", "text": "ID"},
            {"value": "position", "text": "Position"},
            {"value": "name", "text": 'Name'},
            {"value": "weight", "text": "Weight"},
            {"value": "symbol", "text": 'Symbol'},
            {"value": "address", "text": 'Address'}
        ]
        
        items = User.query.all()
        
        resp = {
            "items": UserSchema(many=True).dump(items),
            "headers": headers
        }
        
        return jsonify(resp)
    
    @staticmethod
    def create():
        data = request.json
        user = User()
        
        if data.get('name'):
            user.name = data.get('name')
        
        if data.get('position'):
            user.position = data.get('position')
        
        if data.get('weight'):
            user.weight = data.get('weight')
        
        if data.get('symbol'):
            user.symbol = data.get('symbol')
        
        db.session.add(user)
        db.session.commit()
        
        return UserSchema().dump(user)

    @staticmethod
    def get_for_edit(id):
        user = User.query.get(id)
        return UserSchema().dump(user)

    @staticmethod
    def edit(id):
        data = request.json
        user = User.query.get(id)
    
        if data.get('name'):
            user.name = data.get('name')
    
        if data.get('position'):
            user.position = data.get('position')
    
        if data.get('weight'):
            user.weight = data.get('weight')
    
        if data.get('symbol'):
            user.symbol = data.get('symbol')
        
        db.session.commit()
        return UserSchema().dump(user)

    @staticmethod
    def delete(id):
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return 'True'
