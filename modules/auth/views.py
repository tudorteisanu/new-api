from flask import render_template
from config.settings import app


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')


@app.route('/reset_password')
def reset_password():
    return render_template('reset_password.html')


@app.route('/')
# @auth_required()
def index():
    return render_template('index.html')