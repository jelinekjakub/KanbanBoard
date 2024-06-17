import enum
from flask import flash, request, render_template, redirect
from passlib.hash import pbkdf2_sha256
from app import db
from datetime import datetime
from app.helpers import start_session, clear_session


class ProjectStatus(enum.Enum):
    FINISHED = "Hotovo"
    ACTIVE = "Aktivní"
    PLANNED = "Plánovaný"
    DELAYED = "Zpožděný"


class TaskStatus(enum.Enum):
    TO_DO = "Udělat"
    IN_PROGRESS = "V průběhu"
    FINISHED = "Hotovo"


class TeamRoles(enum.Enum):
    LEADER = "Leader"
    MEMBER = "Člen"


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=True)
    team_role = db.Column(db.Enum(TeamRoles), nullable=True)
    invites = db.relationship("TeamInvite", backref="user", lazy=True)


    def register(self):
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        if User.query.filter_by(email=email).first():
            return (
                render_template(
                    "register.html", message="Tento email již někdo používá"
                ),
                400,
            )

        hashed_password = pbkdf2_sha256.hash(password)

        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return start_session(new_user)

    def login(self):
        user = User.query.filter_by(email=request.form["email"]).first()
        if user and pbkdf2_sha256.verify(request.form["password"], user.password):
            return start_session(user)
        else:
            return (
                render_template("login.html", message="Nesprávné jméno nebo heslo"),
                401,
            )

    def logout(self):
        clear_session()
        return redirect("/")
    
    def change_team(self, team_id, team_role):
        self.team_id = team_id
        self.team_role = team_role


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date, nullable=False, default=datetime.today)
    deadline_date = db.Column(db.Date, nullable=True)
    tasks = db.relationship("Task", backref="project", lazy=True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False)

    @property
    def days_passed(self):
        date_diff = datetime.today().date() - self.start_date
        return date_diff.days if date_diff.days > 0 else 0

    @property
    def task_count(self):
        return Task.query.filter(Task.project_id == self.id).count()

    @property
    def status(self):
        project_tasks = Task.query.filter(Task.project_id == self.id)
        project_tasks_count = project_tasks.count()
        todo_tasks_count = project_tasks.filter(
            Task._status == TaskStatus.TO_DO
        ).count()
        finished_tasks_count = project_tasks.filter(
            Task._status == TaskStatus.FINISHED
        ).count()
        if project_tasks_count == 0 or project_tasks_count == todo_tasks_count:
            return ProjectStatus.PLANNED
        elif project_tasks_count == finished_tasks_count:
            return ProjectStatus.FINISHED
        elif self.deadline_date < datetime.now().date():
            return ProjectStatus.DELAYED
        else:
            return ProjectStatus.ACTIVE


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=False, default=datetime.today)
    finished_date = db.Column(db.Date, nullable=True)
    deadline_date = db.Column(db.Date, nullable=True)
    _status = db.Column(db.Enum(TaskStatus), nullable=False, default=TaskStatus.TO_DO)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status):
        self._status = new_status
        if new_status == TaskStatus.FINISHED:
            self.finished_date = datetime.today()

    def __init__(
        self,
        name,
        description=None,
        start_date=None,
        finished_date=None,
        deadline_date=None,
        status=TaskStatus.TO_DO,
        project_id=None,
    ):
        self.name = name
        self.description = description
        self.start_date = start_date if start_date else datetime.today()
        self.finished_date = finished_date
        self.deadline_date = deadline_date
        self._status = status
        self.project_id = project_id


class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    projects = db.relationship("Project", backref="team", lazy=True)
    members = db.relationship("User", backref="team", lazy=True)
    invites = db.relationship("TeamInvite", backref="team", lazy=True)


class TeamInvite(db.Model):
    __tablename__ = "team_invites"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'team_id', name='_user_team_uc'),
    )
    
    def __init__(self, user_id, team_id):
        self.user_id = user_id
        self.team_id = team_id
