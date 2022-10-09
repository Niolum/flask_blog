import os
from dotenv import load_dotenv


BASE_DIR= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, '.env'))

database_url = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser=os.environ['DBUSER'],
    dbpass=os.environ['DBPASS'],
    dbhost=os.environ['DBHOST'],
    dbname=os.environ['DBNAME']
)
secret_key = os.environ['SECRET_KEY']

SQLALCHEMY_DATABASE_URI = database_url
SECRET_KEY=secret_key

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = database_url
    SECRET_KEY=secret_key

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL")


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,

    'default': DevelopmentConfig
}