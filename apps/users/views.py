from flask import request
from flask import jsonify
from settings import db
from apps.users.models import User
from apps.users.schema import UserSchema
from helpers.auth_utils import auth_required


class UserRoute(object):
    @staticmethod
    @auth_required()
    def get_data():
        headers = [
            {"value": "id", "text": "ID"},
            {"value": "name", "text": 'Name'},
            {"value": "email", "text": "Email"},
            {"value": "role", "text": "Role"}
        ]
        
        params = request.args
        
        items = User \
            .query \
            .order_by(User.id.desc()) \
            .paginate(page=int(params['page']), per_page=int(params['per_page']), error_out=False)
        
        resp = {
            "items": UserSchema(many=True).dump(items.items),
            "pages": items.pages,
            "total": items.total,
            "headers": headers
        }
        
        return jsonify(resp)
    
    @staticmethod
    @auth_required()
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
    @auth_required()
    def get_for_edit(id):
        user = User.query.get(id)
        return UserSchema().dump(user)
    
    @staticmethod
    @auth_required()
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
    @auth_required()
    def delete(id):
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Successful deleted!'}), 200

   