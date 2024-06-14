from flask import Flask
from decouple import config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


app.config.from_object(config("APP_SETTINGS"))
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes
from app import template_filters

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()