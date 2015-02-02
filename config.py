import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db') # Required by Flask-SQLAlchemy extention. Path for the database file.
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository') # Place where we store the SQLAlchemy-migrate data files.
