from flask import request
from flask import jsonify, make_response
from settings import db
from apps.clients.models import Client, validations
from apps.clients.schema import ClientSchema


class ClientRoute(object):
    @staticmethod
    def get_data():
        headers = [
            {"value": "id", "text": "ID"},
            {"value": "name", "text": 'Name'},
            {"value": "text", "text": "Text"},
            {"value": "email", "text": "Email"}
        ]

        params = request.args
        filters = {}
        
        items = Client\
            .query\
            .filter_by(**filters)\
            .order_by(Client.id.desc())\
            .paginate(page=int(params['page']), per_page=int(params['per_page']), error_out=False)
        
        resp = {
            "items": ClientSchema(many=True).dump(items.items),
            "pages": items.pages,
            "total": items.total,
            "headers": headers
        }
        
        return jsonify(resp)
    
    @staticmethod
    def create():
        data = request.json
        user = Client()

        errors = validate(data)

        if len(errors):
            return jsonify({'message': "Invalid data", "errors": errors}), 422
        
        if data.get('name'):
            user.name = data.get('name')
        
        if data.get('email'):
            user.email = data.get('email')
        
        if data.get('text'):
            user.text = data.get('text')
        
        db.session.add(user)
        db.session.commit()
        
        return ClientSchema().dump(user)

    @staticmethod
    def get_for_edit(id):
        client = Client.query.get(id)
        return ClientSchema().dump(client)

    @staticmethod
    def edit(id):
        data = request.json
        client = Client.query.get(id)

        errors = validate(data)

        if len(errors):
            return jsonify({'message': "Invalid data", "errors": errors}), 422
    
        if data.get('email'):
            client.email = data.get('email')
    
        if data.get('name'):
            client.name = data.get('name')
        
        if data.get('text'):
            client.text = data.get('text')
            
        db.session.commit()
        return ClientSchema().dump(client)

    @staticmethod
    def delete(id):
        client = Client.query.get(id)
        db.session.delete(client)
        db.session.commit()
        return jsonify({"message": 'Successfull delete'})


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
                    
                    print(len(field) < minimal_length)
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