from flask import render_template

from app import app


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('/login.html')


@app.route('/register')
def register():
    return render_template('register.html')