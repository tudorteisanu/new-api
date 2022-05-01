from src.modules.degrees.models import Degree
from src.app import db, app

data = [
    {
        "name": "Fara grad"
    },
    {
        "name": "Grad I"
    },
    {
        "name": "Grad II"
    },
    {
        "name": "Grad superior"
    }
]


class DegreesSeeder:
    seeder = []

    def __init__(self):
        self.seeder = []
        self.name = __name__

    def __call__(self):
        with app.app_context():
            print("DegreesSeeder is running...")
            for item in data:
                if not (Degree.query.filter_by(name=item['name']).first()):
                    self.seeder.append(Degree(name=item['name']))
            db.session.add_all(self.seeder)
            db.session.commit()


degree_seeder = DegreesSeeder()
