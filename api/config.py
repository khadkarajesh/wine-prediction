from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config(object):
    TESTING = False
    DB_SERVER = ''


class ProductionConfig(Config):
    DB_SERVER = ''
    SQLALCHEMY_DATABASE_URI = ''


class DevelopmentConfig(Config):
    DB_SERVER = 'localhost'
    SQLALCHEMY_DATABASE_URI = f"postgresql://{environ.get('USER_NAME')}:{environ.get('USER_PASSWORD')}@{DB_SERVER}:{environ.get('DATABASE_PORT')}/{environ.get('DATABASE_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DB_SERVER = 'localhost'
    DATABASE_URI = 'sqlite:///:memory:'
