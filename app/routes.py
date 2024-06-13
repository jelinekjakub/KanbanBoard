from flask import render_template, request
from app import app
from app.models import User
from app.helpers import auth


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return User().login()
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return User().register()
    else:
        return render_template('register.html')


@app.route('/logout')
def logout():
    return User().logout()


@app.route('/board')
@auth
def board():
    return render_template('board.html')


@app.route('/task')
def task_show():
    # id
    return render_template('task/show.html')


@app.route('/task/edit')
def task_edit():
    # id
    return render_template('task/edit.html')


@app.route('/projects')
@auth
def project_index():
    return render_template('project/index.html')
