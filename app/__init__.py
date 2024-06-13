from flask import Flask


app = Flask(__name__)

from app import routes
from app.database import init_db, db_session


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


init_db()
app.secret_key = 'top secret key'
app.run(debug=True)
