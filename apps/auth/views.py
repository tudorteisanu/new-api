from flask_restful import Resource
from settings import db
from apps.users.models import User
from apps.users.schema import UserSchema
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify, abort, g
from flask_jwt_extended import create_access_token
from helpers.auth_utils import auth_required


def send_email_link(email):
    print(f'send link to {email}')


class AuthRoute:
    @staticmethod
    def register():
        data = request.args
        current_user = User.query.filter_by(email=data['email']).first()
        if current_user is not None:
            return jsonify({'message': 'user_exists'}), 401
        
        elif current_user is None:
            user = User(
                name=data['name'],
                email=data['email'],
                password_hash=generate_password_hash(data['password'])
            )
            
            if data and data.get('role', None) is not None:
                user.role = data['role']
            db.session.add(user)
            db.session.commit()
            return jsonify(UserSchema(only=['id', 'name', 'email', 'role']).dump(user))
    
    @staticmethod
    def login():
        data = request.args
        user = User.query.filter_by(email=data['email']).first()
        
        if user is not None:
            if check_password_hash(user.password_hash, data['password']):
                user_agent = request.user_agent
                token = create_access_token(user.id, user_claims={"role": user.role})
                user.token = token
                user.platform = user_agent.platform
                user.browser = user_agent.browser
                db.session.commit()
                data = UserSchema(exclude=['password_hash']).dump(user)
                data['gmail'] = data['email']
                return jsonify(data)
            
            return jsonify({'message': "user not found"}), 401
        abort(404)
        
    @staticmethod
    def forgot_password_step_1():
        data = request.args
        
        email = data.get('email', None)
        
        if email:
            send_email_link(email)
    
    @staticmethod
    def forgot_password_step_2():
        pass
    
    @staticmethod
    def forgot_password_step_3():
        pass
    
    @staticmethod
    def change_password():
        data = request.json
    
        if check_password_hash(g.user.password_hash, data['password']):
            return jsonify({'message': "The new password must not be the same as the old one"}), 422
        else:
            user = User.query.get(g.user.id)
            user.password_hash = generate_password_hash(data['password'])

    @staticmethod
    @auth_required()
    def logout():
        user = User.query.get(g.user.id)
        
        if user is not None:
            user.token = None
            db.session.commit()
        
        return jsonify({"msg": 'success'})

    @staticmethod
    @auth_required()
    def check_token():
        return jsonify({"name": g.user.name, "id": g.user.id, "gmail": g.user.email, "role": g.user.role})


