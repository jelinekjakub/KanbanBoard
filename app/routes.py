from flask import abort, redirect, render_template, request, url_for
from app import app
from app import db
from datetime import date
from app.models import Project, ProjectStatus, Task, TaskStatus, User
from app.helpers import auth


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", menu_page="home")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return User().login()
    else:
        return render_template("login.html", menu_page="login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        return User().register()
    else:
        return render_template("register.html", menu_page="login")


@app.route("/logout")
def logout():
    return User().logout()


@app.route("/board")
@auth
def board():
    task_statuses = list(TaskStatus)
    tasks_list = Task.query.all()
    return render_template("task/board.html", menu_page="tasks", tasks_list=tasks_list, task_statuses=task_statuses)


@app.route("/task")
@auth
def task_show():
    task_id = request.args.get('id')
    task = Task.query.filter(Task.id == task_id).first()
    if not task:
        return abort(404)
    return render_template("task/show.html", menu_page="tasks", task=task)


@app.route("/task/create", methods=["GET", "POST"])
@auth
def task_create():
    if request.method == "POST":
        new_task = Task(
            name=request.form["name"],
            description=request.form["description"],
            deadline_date=date.fromisoformat(request.form["deadline"]),
            project_id=request.form["project"]
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('board'))
    else:
        projects_list = Project.query.filter(Project.status != ProjectStatus.FINISHED).all()
        return render_template("task/create.html", menu_page="tasks", projects_list=projects_list)


@app.route("/task/edit", methods=["GET", "POST"])
@auth
def task_edit():
    task_id = request.args.get('id')
    task = Task.query.filter(Task.id == task_id).first()
    if not task:
        return abort(404)
    if request.method == "POST":
        task.name = request.form["name"]
        task.description = request.form["description"]
        db.session.commit()
        return redirect(f"{url_for('task_show')}?id={task_id}")
    else:
        return render_template("task/edit.html", menu_page="tasks", task=task)

@app.route("/task/delete", methods=["GET"])
@auth
def task_delete():
    task_id = request.args.get('id')
    task = Task.query.filter(Task.id == task_id).first()
    if not task:
        return abort(404)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('board'))

@app.route("/projects")
@auth
def project_index():
    projects = Project.query.all()
    return render_template("project/index.html", menu_page="projects", projects_list=projects)


@app.route("/project/new", methods=["GET", "POST"])
@auth
def project_create():
    if request.method == "POST":
        new_project = Project(
            name=request.form["name"],
            start_date=date.fromisoformat(request.form["date"]),
            deadline_date=date.fromisoformat(request.form["deadline"]),
        )
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('project_index'))
    else:
        context = {"menu_page": "projects"}
        return render_template("project/create.html", context=context)


@app.route("/stats")
@auth
def stats_index():
    return render_template("stats/index.html", menu_page="stats")
