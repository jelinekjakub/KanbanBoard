from flask import session, redirect, url_for, flash
import wrapt

@wrapt.decorator
def auth(wrapped, instance, args, kwargs):
    """Decorator to check if user is authenticated."""
    if 'auth' not in session:
        flash("Pro vstup na tuto stránku musíte být přihlášeni", "info")
        return redirect(url_for('login'))
    return wrapped(*args, **kwargs)

@wrapt.decorator
def has_team(wrapped, instance, args, kwargs):
    """Decorator to check if user has a team."""
    if 'user' not in session:
        return redirect(url_for('login'))

    if 'team_id' not in session['user']:
        return redirect(url_for('team_overview'))

    return wrapped(*args, **kwargs)

def start_session(user):
    """Start a session for the user."""
    session['auth'] = True
    session['user_id'] = user.id
    session['user'] = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
    }
    if user.team_id is not None:
        session['user']['team_id'] = user.team_id
    return redirect(url_for('index'))

def clear_session():
    """Clear the session."""
    session.clear()
    return redirect('/')
