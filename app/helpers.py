from flask import session, redirect, url_for
import wrapt


# Decorators
@wrapt.decorator
def auth(wrapped=None, instance=None, args=None, kwargs=None):
    if 'auth' not in session:
        return redirect(url_for('login'))
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
