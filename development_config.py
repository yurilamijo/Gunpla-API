import os

# ENV = 'development',
# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
# SQLALCHEMY_TRACK_MODIFICATIONS = False
# PROPAGATE_EXCEPTIONS = True
# JWT_BLACKLIST_ENABLED = True
# JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
# SECRET_KEY = b'\x8d\xc1\xa0.\xc2\xf2D\xa6\xea\x1f!\x13\x04\x9c\x13w'

ENV = 'development'  
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
SECRET_KEY = os.environ["APP_SECRET_KEY"]