from decouple import config

DATABASE_URI = config("DATABASE_URL")

class Config(object):
    CSRF_ENABLED = True
    SECRET_KEY = config("SECRET_KEY", default="secret")
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
