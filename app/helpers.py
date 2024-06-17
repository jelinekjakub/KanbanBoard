from flask import session, redirect, url_for, flash
import wrapt


# Decorators
@wrapt.decorator
def auth(wrapped=None, instance=None, args=None, kwargs=None):
    if 'auth' not in session:
        flash("Pro vstup na tuto stránku musíte být přihlášeni", "info")
        return redirect(url_for('login'))
    return wrapped(*args, **kwargs)


@wrapt.decorator
def has_team(wrapped=None, instance=None, args=None, kwargs=None):
    if not session['user']:
        return redirect(url_for('login'))

    if 'team' not in session['user'].keys():
        # flash("Pro vstup musíte mít team", "info")
        return redirect(url_for('no_team'))

    return wrapped(*args, **kwargs)


def start_session(user):
    session['auth'] = True
    session['user_id'] = user.id
    session['user'] = {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }
    return redirect(url_for('index'))


def clear_session():
    session.clear()
    return redirect('/')
