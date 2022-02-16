from config.settings import migrate
import os


def make_models(rootDir='modules', models='models'):
    if os.path.exists(rootDir):
        classes = []
        
        for item in os.listdir(rootDir):
            model = rootDir + '/' + item + '/' + models + '.py'
            if os.path.exists(model):
                with open(model, 'r') as f:
                    lines = f.readlines()
                    classes.extend([{"model": rootDir + '.' + item + '.' + models,
                                     "klass": '{}'.format(line.split()[1].split('(')[0])} for line in lines if
                                    line.startswith('class')])
        [__import__(item['model'], fromlist=["{}".format(item['klass'])]) for item in classes]


if __name__ == '__main__':
    make_models()
    migrate.run()

# Инициализация:            python manage.py db init
# Подготовка к миграции:    python manage.py db migrate
# Миграция:                 python manage.py db upgrade
