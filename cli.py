import unittest
import os
import click
from settings import app
from flask.cli import AppGroup

user_cli = AppGroup('user')

@app.cli.command("new")
@click.argument("name")
def create_app(name):
    filename = "apps/" + str(name)
    os.makedirs(filename, exist_ok=True)
    if os.path.exists(filename):
        create_files(name, filename)
    else:
        print('app "{}" exists!!!'.format(name))


@app.cli.command("runtests")
def run_tests():
    import_tests()
    if __name__ == '__main__':
        unittest.main()


app.cli.add_command(user_cli)

'''
В начале
export FLASK_APP=cli.py
'''

def create_files(name, filename):
    files = ['models.py', 'urls.py', 'schema.py', 'views.py']
    with open(filename + '/models.py', "w") as t:
        t.write(
f'''from settings import db
from sqlalchemy.dialects.postgresql import JSONB

class {name.capitalize()}(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, default='')
''')

    with open(filename + '/urls.py', "w") as t:
        t.write(
f'''from settings import app
from .views import {name}_get_data
from .views import {name}_get_for_edit
from .views import {name}_create
from .views import {name}_edit
from .views import {name}_delete

app.route('/{name}', methods=['GET'])({name}_get_data)
app.route('/{name}/<id>/edit', methods=['GET'])({name}_get_for_edit)
app.route('/{name}', methods=['POST'])({name}_create)
app.route('/{name}/<id>', methods=['PATCH'])({name}_edit)
app.route('/{name}', methods=['DELETE'])({name}_delete)
'''
)

    with open(filename + '/schema.py', "w") as t:
        t.write(f'from settings import ma\nfrom apps.{name}.models import {name.capitalize()} \
        \n\n\nclass {name.capitalize()}Schema(ma.SQLAlchemyAutoSchema):\n \
        \n\tclass Meta: \
        \n\t\tmodel = {name.capitalize()}')

    with open(filename + '/views.py', "w") as t:
        t.write(
f'''from flask import request
from flask import jsonify
from settings import db
from apps.{name}.models import {name.capitalize()}
from apps.{name}.schema import {name.capitalize()}Schema


def {name}_get_data():
    headers = [
        {'{"value": "id", "text": "ID"}'},
        {'{"value": "name", "text": "Name"}'},
    ]
    
    items = {name.capitalize()}.query.all()
    data = {name.capitalize()}Schema(many=True).dump(items)
    
    resp = {
        '{ "items": data, "headers": headers }'
    }
    
    return jsonify(resp)


def {name}_create():
    data = request.json
    {name} = {name.capitalize()}()
    
    if data.get('name'):
        {name}.name = data.get('name')
    
    db.session.add({name})
    db.session.commit()
    
    return {name.capitalize()}Schema().dump({name})


def {name}_get_for_edit(id):
    {name} = {name.capitalize()}.query.get(id)
    return {name.capitalize()}Schema().dump({name})


def {name}_edit(id):
    data = request.json
    {name} = {name.capitalize()}.query.get(id)

    if data.get('name'):
        {name}.name = data.get('name')
    
    db.session.commit()
    return {name.capitalize()}Schema().dump({name})


def {name}_delete():
    item_id = request.args.get('id')
    {name} = {name.capitalize()}.query.get(item_id)
    db.session.delete({name})
    db.session.commit()
    return True

''')

    with open(filename + '/tests.py', "a") as t:
        t.write('from settings import app\n\n#your tests here'.format(
            name.lower(), name.capitalize()))
    print('app <{}> created succesful!'.format(name))


def import_tests(rootDir='apps', models='tests'):
    if os.path.exists(rootDir):
        for item in os.listdir(rootDir):
            model = rootDir + '/'+item+'/'+models+'.py'
            text = 'test module: {}'.format(item)
            nr = int(((100-len(text))/2))
            print('='*nr, text, '='*nr)
            os.system('python -m unittest {}'.format(model))
    else:
        print('no apps found')
