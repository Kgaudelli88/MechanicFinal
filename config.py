import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = 'SimpleCache'

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'mysql+mysqlconnector://root:Trinity2010@localhost/mechanic_shop')
    CACHE_TYPE = 'SimpleCache'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI', 'sqlite:///:memory:')
    CACHE_TYPE = 'SimpleCache'
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'postgresql://final_project_8iq6_user:abXrH1mbcuYHnSnijpxHtnvT7teouRUq@dpg-d51h90mmcj7s73a4v2kg-a.oregon-postgres.render.com/final_project_8iq6')
    CACHE_TYPE = 'RedisCache'