from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_assets import Environment, Bundle


bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate(render_as_batch=True)
assets = Environment()


def create_app() -> Flask:
    from config import active_configuration
    
    app = Flask(
        __name__.split('.')[0],
        static_folder=active_configuration.STATIC_FOLDER,
        static_url_path=active_configuration.STATIC_URL_PATH
    )
    app.config.from_object(active_configuration)
    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app: Flask):
    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    assets.init_app(app)
    with app.app_context():
        scss = Bundle('scss/style.scss', filters='libsass', output='css/style.css')
        assets.register('css_all', scss)


def register_blueprints(app: Flask):
    from client.views import webapp_bp
    from api import api_bp

    app.register_blueprint(webapp_bp, url_prefix='/')
    app.register_blueprint(api_bp, url_prefix='/api')
