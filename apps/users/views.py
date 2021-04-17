from flask import request
from flask import jsonify
from settings import db
from apps.users.models import User
from apps.users.schema import UserSchema


class UserRoute(object):
    @staticmethod
    def get_data():
        headers = [
            {"value": "id", "text": "ID"},
            {"value": "name", "text": 'Name'},
            {"value": "email", "text": "Email"},
            {"value": "role", "text": "Role"}
        ]
        
        items = User.query.all()
        
        resp = {
            "items": UserSchema(many=True, only=("name", "email", "role", 'id')).dump(items),
            "headers": headers
        }
        
        return jsonify(resp)
    
    @staticmethod
    def create():
        data = request.json
        user = User()
        
        if data.get('name'):
            user.name = data.get('name')
        
        if data.get('email'):
            user.email = data.get('email')
        
        if data.get('role'):
            user.role = data.get('role')
        
        db.session.add(user)
        db.session.commit()
        
        return UserSchema(only=("name", "email", "role", 'id')).dump(user)

    @staticmethod
    def get_for_edit(id):
        user = User.query.get(id)
        return UserSchema().dump(user)

    @staticmethod
    def edit(id):
        data = request.json
        user = User.query.get(id)
    
        if data.get('email'):
            user.email = data.get('email')
    
        if data.get('name'):
            user.name = data.get('name')
    
        if data.get('role'):
            user.role = data.get('role')
        
        db.session.commit()
        return UserSchema(only=("name", "email", "role", 'id')).dump(user)

    @staticmethod
    def delete(id):
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return 'True'
