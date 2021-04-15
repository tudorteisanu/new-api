from flask import request
from flask import jsonify
from settings import db
from apps.centers.models import Center
from apps.centers.schema import CenterSchema


class CenterRoute(object):
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
        
        items = Center.query.all()
        
        resp = {
            "items": CenterSchema(many=True).dump(items),
            "headers": headers
        }
        
        return jsonify(resp)

    @staticmethod
    def create():
        data = request.json
        user = Center()
        
        if data.get('name'):
            user.name = data.get('name')
        
        if data.get('position'):
            user.position = data.get('position')
        
        if data.get('weight'):
            user.weight = data.get('weight')
        
        if data.get('symbol'):
            user.symbol = data.get('symbol')
        #
        # if (data.get('address')):
        #     user.name = data.get('address')
        
        db.session.add(user)
        db.session.commit()
        
        return CenterSchema().dump(user)

    @staticmethod
    def get_for_edit(id):
        user = Center.query.get(id)
        return CenterSchema().dump(user)

    @staticmethod
    def edit(id):
        data = request.json
        user = Center.query.get(id)
        
        if data.get('name'):
            user.name = data.get('name')

        if data.get('position'):
            user.position = data.get('position')

        if data.get('weight'):
            user.weight = data.get('weight')

        if data.get('symbol'):
            user.symbol = data.get('symbol')
        
        db.session.commit()
        return CenterSchema().dump(user)

    @staticmethod
    def delete():
        user_id = request.args.get('id')
        user = Center.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return True
