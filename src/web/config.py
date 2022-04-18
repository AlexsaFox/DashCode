import os
import datetime

base_dir = os.getcwd()


class Config:
    # Secret key, used to sign session cookies and API tokens
    SECRET_KEY = os.getenv('SECRET_KEY', 'ladadadada')

    # If set to True (the default) Flask-SQLAlchemy will track
    # modifications of objects and emit signals. This requires
    # extra memory and can be disabled if not needed. Will be
    # disabled by default in the future.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Time before browser session expiration
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=30)

    # Time before API token expiration
    API_TOKEN_LIFETIME = datetime.timedelta(days=30)
    
    # Uploads folder
    UPLOAD_FOLDER = os.path.join(base_dir, 'uploads')

    # Name of file inside of UPLOADS_FOLDER for default user picture
    DEFAULT_USER_PICTURE_FILENAME = 'default.jpeg'

    # File extensions that user can upload as profile pictures
    # Here are all common web image formats
    # https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Image_types
    ALLOWED_FILE_EXTENSIONS = {
        'apng', 'avif', 'gif', 'jpg', 'jpeg', 'jfif', 
        'pjpeg', 'pjp', 'png', 'svg', 'webp'
    }

    # Max size of uploaded file. If larger, 413 "Request entity is too large"
    # error is raised by Flask. Currently set to 16MB
    MAX_CONTENT_LENGTH = 16 * 1000 * 1000

    # Path for serving static files
    STATIC_URL_PATH = '/static'

    # Folder on system containing static files
    STATIC_FOLDER = os.path.join(base_dir, 'client', 'static')

    # .scss files that must be compiled
    # Is relative to STATIC_FOLDER
    ASSETS_SCSS_FILES = ['scss/*.scss']


def build_production_db_uri():
    """ Builds uri for production database using environment variables. """
    dialect = 'postgresql'
    user = os.getenv('DB_USER')
    passwd = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    database = os.getenv('DB_NAME')
    uri = f'{dialect}://{user}:{passwd}@{host}/{database}'
    return uri

class ProductionConfig(Config):
    # Run flask in production mode
    DEBUG = False

    # URI of SQLAlchemy database, is build using environmemnt variables
    SQLALCHEMY_DATABASE_URI = build_production_db_uri()


class DevelopmentConfig(Config):
    # Run flask in debug mode
    DEBUG = True

    # URI of SQLALchemy database, uses local sqlite db for development
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'development.sqlite')


mapping = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
}
active_configuration_type = os.getenv('FLASK_ENV', 'development')
active_configuration: Config = mapping[active_configuration_type]
