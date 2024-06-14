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

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)

    def register(self):
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            return render_template('register.html', message="Tento email již někdo používá"), 400

        hashed_password = pbkdf2_sha256.hash(password)

        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return start_session(new_user)

    def login(self):
        user = User.query.filter_by(email=request.form['email']).first()
        if user and pbkdf2_sha256.verify(request.form['password'], user.password):
            return start_session(user)
        else:
            return render_template('login.html', message="Nesprávné jméno nebo heslo"), 401

    def logout(self):
        clear_session()
        return redirect('/')
    
class Project(db.Model): 
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date, nullable=False, default=datetime.today())
    finished_date = db.Column(db.Date, nullable=True)
    deadline_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.Enum(ProjectStatus), nullable=False, default=ProjectStatus.PLANNED)
    task = db.relationship('Task', backref='project', lazy=True)
    
    @property
    def days_passed(self): 
        date_diff = datetime.today().date() - self.start_date
        return date_diff.days
    
    @property
    def task_count(self): 
        return Task.query.filter(Task.project_id == self.id, Task.status != TaskStatus.FINISHED).count()
    
class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=False, default=datetime.today())
    finished_date = db.Column(db.Date, nullable=True)
    deadline_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.Enum(TaskStatus), nullable=False, default=TaskStatus.TO_DO)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'),
        nullable=False)
