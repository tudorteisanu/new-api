from flask import request
from flask import jsonify
from settings import db
from apps.products.models import Products
from apps.products.schema import ProductsSchema


def products_get_data():
    headers = [
        {"value": "id", "text": "ID",
        "value": "name", "text": "Name"},
    ]
    
    items = Products.query.all()
    data = ProductsSchema(many=True).dump(items)
    
    resp = { "items": data, "headers": headers }
    
    return jsonify(resp)


def products_create():
    data = request.json
    products = Products()
    
    if data.get('name'):
        products.name = data.get('name')
    
    db.session.add(products)
    db.session.commit()
    
    return ProductsSchema().dump(products)


def products_get_for_edit(id):
    products = Products.query.get(id)
    return ProductsSchema().dump(products)


def products_edit(id):
    data = request.json
    products = Products.query.get(id)

    if data.get('name'):
        products.name = data.get('name')
    
    db.session.commit()
    return ProductsSchema().dump(products)


def products_delete():
    item_id = request.args.get('id')
    products = Products.query.get(item_id)
    db.session.delete(products)
    db.session.commit()
    return True

