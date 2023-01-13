import os

basedir = os.environ.get("DB_PARENT_PATH", os.path.abspath(os.path.dirname(__file__)))
DATABASE_PATH = os.path.join(basedir, 'data.sqlite')
print(DATABASE_PATH)

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    
