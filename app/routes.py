from flask import abort, flash, redirect, render_template, request, url_for, session
from sqlalchemy import or_
from app import app
from app import db
from datetime import date
from app.models import Project, ProjectStatus, Task, TaskStatus, Team, TeamInvite,  TeamRoles, User
from app.helpers import auth, has_team, start_session


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
    projects = Project.query_user_projects(session['user_id']).all()
    if not projects:
        flash("Nejprve si musíte založit projekt!", "info")
        return redirect(url_for("project_create"))
    
    project_id = request.args.get('project', projects[0].id)
    project = Project.query_user_projects(session['user_id']).filter(Project.id == project_id).first()
    if not project:
        return abort(404)
    
    tasks_list = Task.query.filter(Task.project_id == project.id)
    task_statuses = list(TaskStatus)    
    return render_template("task/board.html", menu_page="tasks", tasks_list=tasks_list, task_statuses=task_statuses, projects_list = projects, current_project=project)


@app.route("/task", methods=["GET", "POST"])
@auth
def task_show():
    task_id = request.args.get('id')
    task = Task.query.filter(Task.id == task_id).first()
    if not task or not task.has_access(session['user_id']):
        return abort(404)        
    if request.method == "POST":
        task.status = TaskStatus[request.form['status']]
        db.session.commit()
        flash("Změna statusu proběhla úspěšně.", "success")
        return redirect(f"{url_for('task_show')}?id={task_id}")
    else:
        return render_template("task/show.html", menu_page="tasks", task=task)


@app.route("/task/create", methods=["GET", "POST"])
@auth
def task_create():
    if request.method == "POST":
        project_id=request.form["project"]
        if not Project.query_user_projects(session['user_id']).filter(Project.id == project_id).first():
            flash("Tento projekt neexistuje!", "danger")
            return redirect(f"{url_for('board')}")
        new_task = Task(
            name=request.form["name"],
            description=request.form["description"],
            difficulty=request.form["difficulty"],
            deadline_date=date.fromisoformat(request.form["deadline"]),
            project_id=project_id
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(f"{url_for('board')}?project={project_id}")
    else:
        projects_list = Project.query_user_projects(session['user_id']).filter(Project.status != ProjectStatus.FINISHED).all()
        if not projects_list:
            flash("Nejprve si musíte založit projekt!", "info")
            return redirect(url_for("project_create"))
    
        current_project_id = request.args.get('project', projects_list[0].id)
        return render_template("task/create.html", menu_page="tasks", projects_list=projects_list, current_project_id=current_project_id)


@app.route("/task/edit", methods=["GET", "POST"])
@auth
def task_edit():
    task_id = request.args.get('id')
    task = Task.query.filter(Task.id == task_id).first()
    if not task or not task.has_access(session['user_id']):
        return abort(404)
    if request.method == "POST":
        task.name = request.form["name"]
        task.description = request.form["description"]
        task.difficulty = request.form["difficulty"]
        db.session.commit()
        return redirect(f"{url_for('task_show')}?id={task_id}")
    else:
        return render_template("task/edit.html", menu_page="tasks", task=task)


@app.route("/task/delete", methods=["GET"])
@auth
def task_delete():
    task_id = request.args.get('id')
    task = Task.query.filter(Task.id == task_id).first()
    task_project_id = task.project_id
    if not task or not task.has_access(session['user_id']):
        return abort(404)
    db.session.delete(task)
    db.session.commit()
    return redirect(f"{url_for('board')}?project={task_project_id}")


@app.route("/projects")
@auth
def project_index():
    projects = Project.query_user_projects(session['user_id']).all()
    return render_template("project/index.html", menu_page="projects", projects_list=projects)


@app.route("/project/new", methods=["GET", "POST"])
@auth
def project_create():
    if request.method == "POST":
        new_project = Project(
            name=request.form["name"],
            start_date=date.fromisoformat(request.form["date"]),
            deadline_date=date.fromisoformat(request.form["deadline"]),
            user_id=session['user_id'],
            team_id=session['user'].get('team_id') if request.form.get("share", False) else None
        )
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('project_index'))
    else:
        return render_template("project/create.html", menu_page="projects")


@app.route("/project/edit", methods=["GET", "POST"])
@auth
def project_edit():
    project_id = request.args.get('id')
    project = Project.query_user_projects(session['user_id']).filter(Project.id == project_id).first()
    if not project:
        return abort(404)
    if request.method == "POST":
        project.name = request.form["name"]
        project.deadline_date = date.fromisoformat(request.form["deadline"])
        db.session.commit()
        flash(f"Projekt {project.name} byl upraven.", "success")
        return redirect(url_for('project_index'))
    else:
        return render_template("project/edit.html", menu_page="projects", project=project)
    

@app.route("/stats")
@auth
def stats_index():
    projects = Project.query_user_projects(session['user_id']).all()
    return render_template("stats/index.html", menu_page="stats", projects=projects)


@app.route("/profile")
@auth
def profile():
    return render_template("profile/index.html", menu_page="profile")


@app.route("/stats/burndown")
@auth
def burndown():
    project = Project.query_user_projects(session['user_id']).filter(Project.id == request.args.get('project')).first()
    if not project:
        return abort(404)
    data = project.get_burndown_data()
    return render_template("stats/burndown.html", menu_page="stats", project=project, data=data)


@app.route("/stats/velocity")
@auth
def velocity():
    project = Project.query_user_projects(session['user_id']).filter(Project.id == request.args.get('project')).first()
    if not project:
        return abort(404)
    data = project.get_velocity_data()
    return render_template("stats/velocity.html", menu_page="stats", project=project, data=data)


@app.route("/team")
@auth
@has_team
def team():
    current_user = User.query.filter(User.id == session['user_id']).first()
    return render_template("team/index.html", menu_page="team", current_user=current_user)


@app.route("/overview")
@auth
def team_overview():
    current_user = User.query.filter(User.id == session['user_id']).first()
    return render_template("team/overview.html", menu_page="team", current_user=current_user)


@app.route("/team/new", methods=["POST"])
@auth
def team_create():
    current_user = User.query.filter(User.id == session['user_id']).first()
    if current_user.team_id is None: 
        new_team = Team(name = request.form["team_name"])
        db.session.add(new_team)
        db.session.commit()
        current_user.change_team(new_team.id, TeamRoles.LEADER)
        db.session.commit()
        start_session(current_user)
    else:
        flash("Nemůžete si založit nový tým, protože již jste členem nějakého týmu.", "danger")
    return redirect(url_for("team"))


@app.route("/team/invite", methods=["POST"])
@auth
@has_team
def team_invite():
    current_user = User.query.filter(User.id == session['user_id']).first()
    if current_user.team_role == TeamRoles.LEADER: 
        invited_user = User.query.filter(User.email == request.form['member_email']).first()
        if not invited_user or invited_user == current_user or invited_user.team_id == current_user.team_id:
            flash("Tohoto uživatele nelze pozvat do teamu!", "danger")
        elif TeamInvite.query.filter(TeamInvite.user_id == invited_user.id, TeamInvite.team_id == current_user.team_id).first():
            flash("Uživatel byl již do tohoto týmu pozván!", "danger")
        else:
            new_invite = TeamInvite(invited_user.id, current_user.team_id)
            db.session.add(new_invite)
            db.session.commit()
            flash(f"Uživateli {invited_user.name} jsme odeslali pozvánku do týmu {current_user.team.name}.", "success")
    else:
        flash("Nemůžete pozvat uživatele do teamu, protože nejste leaderem týmu!", "danger")
    return redirect(url_for("team"))


@app.route("/team/invite_accept", methods=["POST"])
@auth
def team_invite_accept():
    current_user = User.query.filter(User.id == session['user_id']).first()
    team_id = request.form['team_id']
    team_invite = TeamInvite.query.filter(TeamInvite.user_id == current_user.id, TeamInvite.team_id == team_id).first()
    if team_invite and current_user.team_id is None: 
        current_user.change_team(team_id, TeamRoles.MEMBER)
        db.session.delete(team_invite)
        db.session.commit()
        start_session(current_user)
    elif current_user.team_id is not None:
        flash("Nemůžete být členem více týmů!", "danger")
    else:
        flash("Pozvánka to tohoto teamu neexistuje!", "danger")
    return redirect(url_for("team"))


@app.route("/team/leave", methods=["POST"])
@auth
@has_team
def team_leave():
    current_user = User.query.filter(User.id == session['user_id']).first()
    if current_user.team_role != TeamRoles.LEADER:    
        current_user.change_team(None,None)
        flash("Úspěšně jste opustili jste team.", "info")
    else:
        flash("Jako leader nemůžete opustit team!", "danger")
    return redirect(url_for("team_overview"))



@app.route("/team/delete", methods=["POST"])
@auth
@has_team
def team_delete():
    current_user = User.query.filter(User.id == session['user_id']).first()
    if current_user.team_role != TeamRoles.LEADER:  
        flash("Jako pouhý člen nemůžete zrušit team!", "danger")
    else:
        team_to_delete = current_user.team
        for team_member in current_user.team.members:
            team_member.change_team(None,None)
        for team_invite in team_to_delete.invites:
            db.session.delete(team_invite)
        db.session.delete(team_to_delete)
        db.session.commit()
        flash("Úspěšně jste zrušili jste team. Všechny společné projekty byly nastaveny jako privátní.", "info")
    return redirect(url_for("team_overview"))

