import os


base_dir = os.getcwd()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'ladadadada')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def build_production_db_uri():
    dialect = 'postgresql'
    user = os.getenv('DB_USER')
    passwd = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    database = os.getenv('DB_NAME')
    uri = f'{dialect}://{user}:{passwd}@{host}/{database}'
    return uri

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = build_production_db_uri()


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'development.sqlite')


mapping = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
}
active_configuration_type = os.getenv('FLASK_ENV', 'development')
active_configuration = mapping[active_configuration_type]
