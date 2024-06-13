from decouple import config



DATABASE_URI = config("DATABASE_URL")
SECRET_KEY = config("SECRET_KEY", default="topsecret")
SQLALCHEMY_DATABASE_URI = DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

