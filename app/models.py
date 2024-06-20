import enum
from flask import flash, request, render_template, redirect
from passlib.hash import pbkdf2_sha256
from sqlalchemy import func
from app import db
from datetime import datetime, timedelta
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
    projects = db.relationship("Project", backref="user", lazy=True)


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
        for my_project in self.projects:
            if my_project.team_id:
                my_project.team_id = team_id
        self.team_id = team_id
        self.team_role = team_role
        db.session.commit()
        

class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date, nullable=False, default=datetime.today)
    deadline_date = db.Column(db.Date, nullable=True)
    tasks = db.relationship("Task", backref="project", lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=True)

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
    
    @staticmethod
    def query_user_projects(user_id):
        current_user = User.query.filter(User.id == user_id).first()
        if not current_user:
            return Project.query.filter(False)
        user_projects = Project.query.filter(Project.user_id == user_id)
        has_team = current_user.team_id is not None
        if has_team:
            team_projects = Project.query.filter(Project.team_id == current_user.team_id)
            user_projects = user_projects.union(team_projects)
        return user_projects

    def get_burndown_data(self):
        total_work = db.session.query(func.sum(Task.difficulty)).filter(Task.project_id == self.id).one()[0]
        finished_tasks = Task.query.filter(Task.project_id == self.id, Task.finished_date).order_by(
            Task.finished_date).all()

        start_percent = 100
        data = {self.start_date: start_percent}

        for task in finished_tasks:
            start_percent -= (100 / total_work)*task.difficulty
            data[task.finished_date] = start_percent

        # Determine the end date for percent_data to be the current date or the project deadline, whichever is earlier
        project_status = self.status
        if project_status == ProjectStatus.ACTIVE or project_status == ProjectStatus.PLANNED:
            end_date = self.deadline_date
        elif project_status == ProjectStatus.DELAYED:
            end_date = datetime.today().date()
        else:
            end_date = max(self.deadline_date, max(data.keys()))

        percent_days = (end_date - self.start_date).days + 1

        all_dates = [self.start_date + timedelta(days=i) for i in range(percent_days)]

        percent_data = []
        current_percent = 100
        for date in all_dates:
            if date in data:
                current_percent = data[date]
            percent_data.append(current_percent)

            if date == datetime.today().date():
                break
            
        # Create days_all with all days between start_date and end_date
        ideal_total_days = (self.deadline_date - self.start_date).days + 1

        # Create ideal percent data
        ideal_data = [100 - (100 / (ideal_total_days - 1)) * day for day in range(ideal_total_days)]

        real_total_days = (end_date - self.start_date).days + 1
        
        days_all = [f"Den {day}" for day in range(1, real_total_days + 1)]
        data_new = [{'x': 'Den 1', 'y': 100}] + [
                {"x": date, "y": percent} for percent, date in zip(percent_data, days_all)
            ]
        days_diff = real_total_days - ideal_total_days
        ideal_data += [0 for _ in range(days_diff)]
        return {
            "data": data_new,
            "days_all": days_all,
            "ideal_data": ideal_data,
        }

    def get_velocity_data(self):
        finished_tasks = Task.query.filter(Task.project_id == self.id, Task.finished_date.isnot(None)).all()
        all_tasks = Task.query.filter(Task.project_id == self.id).all()

        actual_weekly_data = self._get_weekly_data(finished_tasks, date_attr='finished_date')
        ideal_weekly_data = self._get_weekly_data(all_tasks, date_attr='deadline_date')

        actual_weekly_data = self._fill_missing_weeks(actual_weekly_data)
        ideal_weekly_data = self._fill_missing_weeks(ideal_weekly_data)

        result = {"actual_data": self._transform_weekly_data(actual_weekly_data),
                  "ideal_data": self._transform_weekly_data(ideal_weekly_data)}
        return result

    def _get_weekly_data(self, tasks, date_attr):
        weekly_data = {}
        for task in tasks:
            date = getattr(task, date_attr)
            if date:
                week_number = date.isocalendar()[1]
                year = date.year
                key = (year, week_number)
                if key in weekly_data:
                    weekly_data[key] += task.difficulty
                else:
                    weekly_data[key] = task.difficulty
        return weekly_data

    def _fill_missing_weeks(self, weekly_data):
        start_date = self.start_date
        end_date = self.deadline_date if self.deadline_date else datetime.today().date()
        current_date = start_date

        while current_date <= end_date:
            week_number = current_date.isocalendar()[1]
            year = current_date.year
            key = (year, week_number)
            if key not in weekly_data:
                weekly_data[key] = 0
            current_date += timedelta(days=7 - current_date.weekday())  # Move to next Monday

        return weekly_data

    def _transform_weekly_data(self, data):
        transformed_data = []
        sorted_data = sorted(data.items())
        
        index = 1
        for _, count in sorted_data:
            transformed_data.append({
                "x": f"Týden {index}",
                "y": count,
            })
            index += 1

        transformed_data.append({
                "x": f"Týden {index}",
                "y": 0,
            })

        return transformed_data


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    difficulty = db.Column(db.Integer, db.CheckConstraint('difficulty > 0 AND difficulty < 6'), nullable=False, default=3)
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
        elif self.finished_date is not None:
            self.finished_date = None

    def __init__(
        self,
        name,
        description=None,
        difficulty=None,
        start_date=None,
        finished_date=None,
        deadline_date=None,
        status=TaskStatus.TO_DO,
        project_id=None,
    ):
        self.name = name
        self.description = description
        self.difficulty = difficulty
        self.start_date = start_date if start_date else datetime.today()
        self.finished_date = finished_date
        self.deadline_date = deadline_date
        self._status = status
        self.project_id = project_id
    
    def has_access(self, user_id):
        if self.project.user_id == user_id:
            return True
        current_user = User.query.filter(User.id == user_id).first()
        if current_user and current_user.team_id is not None and self.project.team_id == current_user.team_id:
            return True
        else:
            return False


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
