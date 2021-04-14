import unittest
import os
import click
from settings import app
from flask.cli import AppGroup

user_cli = AppGroup('user')

@app.cli.command("new")
@click.argument("name")
def create_user(name):
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
            "from settings import db\nfrom sqlalchemy.dialects.postgresql import JSONB\n\n# your model here")

    with open(filename + '/urls.py', "w") as t:
        t.write("from settings import db, app, api\nfrom .views import {}Route\n\n#your routes here".format(
            name.capitalize()))

    with open(filename + '/schema.py', "w") as t:
        t.write("from settings import ma\n\n#your schema here")

    with open(filename + '/views.py', "w") as t:
        t.write("from flask_restful import Resource\n\nclass {1}Route(Resource):\n\tdef get(self):\n\t\tpass\n\tdef post(self):\n\t\tpass".format(name, name.capitalize()) +
                "\n\tdef put(self):\n\t\tpass\n\tdef delete(self):\n\t\tpass")

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
