from src.modules.positions.models import Position
from src.app import db, app
from faker import Faker

data = [
    {
        "name": 'Profesor de Limba si literatura Romina'
    },
    {
        "name": 'Profesor de Ed. Fizica',
    },
    {
        "name": 'Profesor de Fizica',
    },
    {
        "name": 'Profesor de Matematica',
    },
    {
        "name": 'Profesor de Ed. tehnologica',
    },
    {
        "name": 'Profesor de Siguranta traficului rutier',
    },
    {
        "name": 'Profesor de Istorie',
    },
    {
        "name": 'Profesor de Arta plastica',
    },
    {
        "name": 'Profesor de Stiinte',
    },
    {
        "name": 'Profesor de Biologie',
    },
    {
        "name": 'Profesor de Limba engleza',
    },
    {
        "name": 'Profesor de Limba Franceza',
    },
    {
        "name": 'Profesor de Limba Germana',
    },
    {
        "name": 'Profesor de Informatica',
    }
]


class PositionsSeeder:
    seeder = []

    def __init__(self):
        self.seeder = []
        self.name = __name__

    def __call__(self):
        with app.app_context():
            print("PositionsSeeder is running...")
            for item in data:
                if not (Position.query.filter_by(name=item['name']).first()):
                    self.seeder.append(Position(name=item['name']))

            for item in range(5000):
                faker = Faker('ro_RO')
                self.seeder.append(Position(name=faker.name()))
            db.session.add_all(self.seeder)
            db.session.commit()


positions_seeder = PositionsSeeder()
