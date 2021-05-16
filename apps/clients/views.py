from flask import request
from flask import jsonify, make_response
from settings import db
from apps.clients.models import Client
from apps.clients.schema import ClientSchema
from helpers.auth_utils import auth_required


class ClientRoute(object):
    @staticmethod
    @auth_required()
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
    @auth_required()
    def create():
        data = request.json
        user = Client()
        
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
    @auth_required()
    def get_for_edit(id):
        client = Client.query.get(id)
        return ClientSchema().dump(client)

    @staticmethod
    @auth_required()
    def edit(id):
        data = request.json
        client = Client.query.get(id)
    
        if data.get('email'):
            client.email = data.get('email')
    
        if data.get('name'):
            client.name = data.get('name')
        
        if data.get('text'):
            client.text = data.get('text')
            
        db.session.commit()
        return ClientSchema().dump(client)

    @staticmethod
    @auth_required()
    def delete(id):
        client = Client.query.get(id)
        db.session.delete(client)
        db.session.commit()
        return jsonify({"message": 'Successful delete'})
