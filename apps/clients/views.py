from flask import request
from flask import jsonify, make_response
from settings import db
from apps.clients.models import Client
from apps.clients.schema import ClientSchema


class ClientRoute(object):
    @staticmethod
    def get_data():
        headers = [
            {"value": "id", "text": "ID"},
            {"value": "name", "text": 'Name'},
            {"value": "text", "text": "Text"}
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
            "headers": headers
        }
        
        return jsonify(resp)
    
    @staticmethod
    def create():
        data = request.json
        user = Client()
        
        if data.get('name'):
            user.name = data.get('name')
        
        if data.get('email'):
            user.email = data.get('email')
        
        if data.get('role'):
            user.role = data.get('role')
        
        if data.get('text'):
            user.text = data.get('text')
        
        db.session.add(user)
        db.session.commit()
        
        return ClientSchema().dump(user)

    @staticmethod
    def get_for_edit(id):
        user = Client.query.get(id)
        return ClientSchema().dump(user)

    @staticmethod
    def edit(id):
        data = request.json
        user = Client.query.get(id)
    
        if data.get('email'):
            user.email = data.get('email')
    
        if data.get('name'):
            user.name = data.get('name')
    
        if data.get('role'):
            user.role = data.get('role')
        
        if data.get('text'):
            user.text = data.get('text')
        
        db.session.commit()
        return ClientSchema().dump(user)

    @staticmethod
    def delete(id):
        user = Client.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": 'Successfull delete'})
        # todo error messages
        # return jsonify({"message": 'An error occured', "errors": [1,2,3,4]}), 422
