from flask import request
from flask import jsonify
from settings import db
from apps.roles.models import Role as Model
from apps.roles.schema import RolesSchema as Schema
from helpers.auth_utils import auth_required


class RolesRoute(object):
    @staticmethod
    @auth_required()
    def get_data():
        headers = [
            {"value": "id", "text": "ID"},
            {"value": "name", "text": 'Name'},
            {"value": "guard", "text": "Guard"},
            {"value": "alias", "text": "Alias"}
        ]

        params = request.args
        
        items = Model\
            .query\
            .order_by(Model.id.desc())\
            .paginate(page=int(params['page']), per_page=int(params['per_page']), error_out=False)
        
        response = {
            "items": Schema(many=True).dump(items.items),
            "pages": items.pages,
            "total": items.total,
            "headers": headers
        }
        
        return jsonify(response)

    
    @staticmethod
    @auth_required()
    def get_list():
        items = Model.query.all()
        return jsonify(Schema(many=True).dump(items))
       
    @staticmethod
    @auth_required()
    def create():
        data = request.json
        user = Model()
        
        if data.get('name'):
            user.name = data.get('name')
        
        if data.get('guard'):
            user.guard = data.get('guard')
        
        if data.get('alias'):
            user.alias = data.get('alias')
        
        db.session.add(user)
        db.session.commit()
        
        return Schema().dump(user)

    @staticmethod
    @auth_required()
    def get_for_edit(id):
        client = Model.query.get(id)
        return Schema().dump(client)

    @staticmethod
    @auth_required()
    def edit(id):
        data = request.json
        client = Model.query.get(id)

        if data.get('name'):
            client.name = data.get('name')

        if data.get('guard'):
            client.guard = data.get('guard')

        if data.get('alias'):
            client.alias = data.get('alias')
            
        db.session.commit()
        return Schema().dump(client)

    @staticmethod
    @auth_required()
    def delete(id):
        client = Model.query.get(id)
        db.session.delete(client)
        db.session.commit()
        return jsonify({"message": 'Successful delete'})
