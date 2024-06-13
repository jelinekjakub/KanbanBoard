from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user

from .forms import LoginForm, RegisterForm

from app import app, bcrypt, db
from app.models import User

@app.route('/')
@app.route('/index')
def index():
    flash("Tohle je jen test alertů ... Doufám, že to funguje ...", "info")
    flash("Alerty mají 3 různé úrovně, danger, success a info ... ", "danger")
    flash("Vypadají nějak takhle ... A dají se i zavřít tím křížkem ... ", "success")
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("Už jste prihlášen(a).", "info")
        return redirect(url_for("index"))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("Neplatná kombinace emailu a hesla.", "danger")
            return render_template("login.html", form=form)
    return render_template('login.html', form=form)


@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("Už jste zaregistrován(a).", "info")
        return redirect(url_for("index"))
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(username=form.username.data,email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash(f"Registrace proběhla úspěšně a jste přihlášen(a).", "success")

        return redirect(url_for("index"))

    return render_template('register.html', form=form)

@app.route('/logout', methods=["GET", "POST"])
def logout():
    logout_user()
    flash("Byl(a) jste odhlášen(a) .", "success")
    return redirect(url_for("index"))


@app.route('/board')
@login_required
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
