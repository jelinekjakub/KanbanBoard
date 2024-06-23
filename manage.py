from flask.cli import FlaskGroup
from app import app

cli = FlaskGroup(app)

import random
from app import db
from app.models import Team, TeamRoles, User, Project, Task, TaskStatus
from datetime import datetime, timedelta
from passlib.hash import pbkdf2_sha256

@app.cli.command('seed_db')
def seed_db():
    # Clear existing data
    db.drop_all()
    db.create_all()

    db.session.add(Team(name="Friends"))

    
    # Add users
    users = [
        User(name="Alice", email="alice@example.com", password=pbkdf2_sha256.hash("password123"), team_id=1, team_role=TeamRoles.LEADER),
        User(name="Bob", email="bob@example.com", password=pbkdf2_sha256.hash("password123"),team_id=1, team_role=TeamRoles.MEMBER),
        User(name="Charlie", email="charlie@example.com", password=pbkdf2_sha256.hash("password123")),
    ]
    db.session.add_all(users)
    db.session.commit()
    
    
    task_count = 30
    
    # Project names
    project_names = ["Project Orion", "Project Nebula", "Project Horizon", "Project Phoenix"]

    # Add projects with specific statuses
    projects = []

    # Active Projects
    for project_name in project_names:  # Total 10 projects including the above three
        project = Project(
            name=project_name,
            start_date=datetime.today() - timedelta(days=random.randint(20, 30)),
            deadline_date=datetime.today() + timedelta(days=random.randint(3, 14)),
            user_id=1,
            team_id=1,
        )
        projects.append(project)
        
    # Delayed Project
    delayed_project = Project(
        name="Project Quantum Leap",
        start_date=datetime.today() - timedelta(days=60),
        deadline_date=datetime.today() - timedelta(days=1),
        user_id=3,
        team_id=None
    )
    projects.append(delayed_project)

    # Finished Project
    finished_project = Project(
        name="Project Lambda",
        start_date=datetime.today() - timedelta(days=60),
        deadline_date=datetime.today() - timedelta(days=30),
        user_id=1,
        team_id=1,
    )
    projects.append(finished_project)

    # Planned Project
    planned_project = Project(
        name="Project Hades",
        start_date=datetime.today(),
        deadline_date=datetime.today() + timedelta(days=60),
        user_id=1,
        team_id=1,
    )
    projects.append(planned_project)




    db.session.add_all(projects)
    db.session.commit()

    # Add tasks
    tasks = []

    # Tasks for Finished Project
    for j in range(task_count):
        task = Task(
            name=f"Task {j+1} for {finished_project.name}",
            description=f"Description for task {j+1} of {finished_project.name}",
            difficulty=random.randint(1,5),
            start_date=finished_project.start_date + timedelta(days=random.randint(0, 10)),
            deadline_date=finished_project.deadline_date - timedelta(days=random.randint(0, 10)),
            status=TaskStatus.FINISHED,
            project_id=finished_project.id,
            finished_date=datetime.today() - timedelta(days=random.randint(1, 30))
        )
        tasks.append(task)

    # Tasks for Planned Project
    for j in range(task_count):
        task = Task(
            name=f"Task {j+1} for {planned_project.name}",
            description=f"Description for task {j+1} of {planned_project.name}",
            difficulty=random.randint(1,5),
            start_date=planned_project.start_date + timedelta(days=random.randint(0, 10)),
            deadline_date=planned_project.deadline_date - timedelta(days=random.randint(0, 10)),
            status=TaskStatus.TO_DO,
            project_id=planned_project.id
        )
        tasks.append(task)

    # Tasks for Additional Projects
    for project in projects[:-2]:
        for j in range(task_count):
            status = random.choice(list(TaskStatus))
            task = Task(
                name=f"Task {j+1} for {project.name}",
                description=f"Description for task {j+1} of {project.name}",
                difficulty=random.randint(1,5),
                start_date=project.start_date + timedelta(days=random.randint(0, 10)),
                deadline_date=project.start_date + timedelta(days=random.randint(10, 30)),
                status=status,
                project_id=project.id
            )
            if status == TaskStatus.FINISHED:
                task.finished_date = task.start_date + timedelta(days=random.randint(1, 19))
            tasks.append(task)

    db.session.add_all(tasks)
    db.session.commit()

    print("Database seeded!")

if __name__ == "__main__":
    cli()
