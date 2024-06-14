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
    return render_template('index.html', menu_page='home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return User().login()
    else:
        return render_template('login.html', menu_page='login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return User().register()
    else:
        return render_template('register.html', menu_page='login')


@app.route('/logout')
def logout():
    return User().logout()


@app.route('/board')
@auth
def board():
    return render_template('task/board.html', menu_page='tasks')


@app.route('/task')
@auth
def task_show():
    # id
    return render_template('task/show.html', menu_page='tasks')


@app.route('/task/create')
@auth
def task_create():
    # id
    return render_template('task/create.html', menu_page='tasks')


@app.route('/task/edit')
@auth
def task_edit():
    # id
    return render_template('task/edit.html', menu_page='tasks')


@app.route('/projects')
@auth
def project_index():
    return render_template('project/index.html', menu_page='projects')


@app.route('/project/new')
@auth
def project_create():
    return render_template('project/create.html', menu_page='projects')
