import hashlib
import os
from random import random
from flask_cors import CORS
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

BACKEND_ADDRESS = 'https://files.testways.online'


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
            if not request.files.get('file', None):
                return jsonify({"message": "Files required"}), 422
            return save_files(request.files['file'])
        except Exception as e:
            print(e)
            return jsonify({"message": "Internal server error"}), 500

    elif request.method == 'GET':
        try:
            return jsonify(os.listdir('static')), 200
        except Exception as e:
            print(e)
            return jsonify({"message": "Internal server error"}), 500


def save_files(file):
    filename = f'{hashlib.md5(secure_filename(file.filename).encode()).hexdigest()}{random()}.{file.filename.split(".")[1]}'
    file.save(os.path.join('static', filename))
    file_path = f'static/{filename}'
    return jsonify({
               "size": os.stat(file_path).st_size,
               "mime-type": file.mimetype,
               "url": f'{BACKEND_ADDRESS}/{file_path}',
               "name": file.filename
           }), 201


if __name__ == '__main__':
    app.run(debug=True)
