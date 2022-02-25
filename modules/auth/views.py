from flask import render_template, redirect
from application import app
from flask_login import login_required, logout_user, current_user


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/change_password')
@login_required
def change_password():
    return render_template('change_password.html')


@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')


@app.route('/reset_password')
def reset_password():
    return render_template('reset_password.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/')
@login_required
def index():
    print(current_user)
    return render_template('index.html')