from flask import request
from flask import jsonify
from settings import db
from apps.users.models import User
from apps.users.models import validations
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
    def create():
        data = request.json
        user = User()
        errors = validate(data)

        if len(errors):
            return jsonify({'message': "Invalid data", "errors": errors}), 422
        
        if data.get('name'):
            user.name = data.get('name')
        
        if data.get('email'):
            user.email = data.get('email')
        
        if data.get('role'):
            user.role = data.get('role')
        
        if len(errors) > 0:
            return jsonify({'message': "Invalid data", "errors": errors}), 422
        
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
        errors = validate(data)
        
        if len(errors):
            return jsonify({'message': "Invalid data", "errors": errors}), 422
        
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

        
def validate(data):
    errors = {}
    for key in validations:
        field_validations = validations[key].split(',')
        
        for validation in field_validations:
            if validation == 'required' and key not in data:
                errors[key] = f'Field {key} is required'
            
            elif key in data:
                field = data[key]
                
                if validation.startswith('min:'):
                    minimal_length = int(validation.split(':')[1])
                    
                    print(len(field)<minimal_length)
                    if len(field) < minimal_length:
                        errors[key] = f'Minimal length is {minimal_length}'

                if validation.startswith('max:'):
                    maximal_length = int(validation.split(':')[1])
    
                    if len(field) > maximal_length:
                        errors[key] = f'Maximal length is {maximal_length}'

                elif validation.startswith('exact:'):
                    exact = int(validation.split(':')[1])
    
                    if len(field) != exact:
                        errors[key] = f'Length must be {exact}'
    return errors
   