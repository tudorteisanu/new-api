FROM kennethreitz/pipenv

COPY . /app

WORKDIR /app

RUN pipenv install --deploy --system

CMD python3 run.py