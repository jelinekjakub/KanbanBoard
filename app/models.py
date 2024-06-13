from flask import request, render_template, redirect
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base, db_session
from passlib.hash import pbkdf2_sha256
from app.helpers import start_session, clear_session


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(50), unique=True, nullable=False)

    def register(self):
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if db_session.query(User).filter_by(email=email).first():
            return render_template('register.html', message="Tento email již někdo používá"), 400

        hashed_password = pbkdf2_sha256.hash(password)

        new_user = User(name=name, email=email, password=hashed_password)
        db_session.add(new_user)
        db_session.commit()

        return start_session(new_user)

    def login(self):
        user = db_session.query(User).filter_by(email=request.form['email']).first()

        if user and pbkdf2_sha256.verify(request.form['password'], user.password):
            return start_session(user)
        else:
            return render_template('login.html', message="Nesprávné jméno nebo heslo"), 401

    def logout(self):
        clear_session()
        return redirect('/')