from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate


bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate()


def create_app() -> Flask:
    from config import active_configuration
    
    app = Flask(__name__.split('.')[0])
    app.config.from_object(active_configuration)
    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app: Flask):
    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app: Flask):
    from client.views import webapp_bp
    from api import api_bp

    app.register_blueprint(webapp_bp)
    app.register_blueprint(api_bp)
