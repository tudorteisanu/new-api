from src.modules.course.models import Course
from src.app import app
from faker import Faker


class CoursesSeeder:
    items = []

    def __init__(self):
        self.name = __name__

    def __call__(self, count=10):
        with app.app_context():
            print('Courses seeder is running..')
            self.seed_courses(count)

    def seed_courses(self, count=30):
        for item in range(count):
            course = Course()

            faker = Faker('en_US')
            course.name = faker.name()
            course.description = faker.text()
            self.items.append(course)


courses_seeder = CoursesSeeder()
