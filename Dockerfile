FROM python:3.8.13-alpine3.15

WORKDIR /var/www/html

COPY requirements.txt .

RUN pip3 install -r requirements.txt

RUN pip3 install gunicorn

COPY  . .

EXPOSE 8000

ENTRYPOINT [ "python" ]

CMD ["app.py" ]