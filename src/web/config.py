import os
import datetime

base_dir = os.getcwd()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'ladadadada')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=30)
    API_TOKEN_LIFETIME = datetime.timedelta(days=30)
    
    UPLOAD_FOLDER = os.path.join(base_dir, 'uploads')
    DEFAULT_USER_PICTURE_FILENAME = 'default.jpeg'
    ALLOWED_FILE_EXTENSIONS = {
        'apng', 'avif', 'gif', 'jpg', 'jpeg', 'jfif', 
        'pjpeg', 'pjp', 'png', 'svg', 'webp'
    }
    MAX_CONTENT_LENGTH = 16 * 1000 * 1000   # 16 MB


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
active_configuration: Config = mapping[active_configuration_type]
