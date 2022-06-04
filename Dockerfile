FROM python:3.8.13-alpine3.15

WORKDIR /var/www/html

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY  . .

EXPOSE 8000

CMD [ "python", "./app.py" ]