import secrets

secret_key = secrets.token_hex(16)
SQLALCHEMY_DATABASE_URI = 'sqlite:///data/db.sqlite3'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = secret_key
CACHE_TYPE = 'simple'