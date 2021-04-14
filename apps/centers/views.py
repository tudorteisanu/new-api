from flask import request
from flask import jsonify
from settings import db
from apps.centers.models import Center
from apps.centers.schema import CenterSchema

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)
        

def get_centers_data():
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


def create_center():
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


def get_center_for_edit(id):
    user = Center.query.get(id)
    return CenterSchema().dump(user)


def edit_center(id):
    data = request.json
    user = Center.query.get(id)

    str = Struct(**data)
    
    user = str
    
    print(user.symbol)
    
    
    # if data.get('name'):
    #     user.name = data.get('name')
    #
    # if data.get('position'):
    #     user.position = data.get('position')
    #
    # if data.get('weight'):
    #     user.weight = data.get('weight')
    #
    # if data.get('symbol'):
    #     user.symbol = data.get('symbol')
    
    db.session.commit()
    return CenterSchema().dump(user)


def delete_center():
    user_id = request.args.get('id')
    user = Center.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return True
