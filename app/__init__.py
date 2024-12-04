# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

login_manager.login_view = 'main.login'

def create_app():
    # Initialize the Flask app
    app = Flask(__name__, template_folder='../templates', static_folder='../static' )

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SECRET_KEY'] = 'SecretKey'
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    
    from app.models import User
    

    with app.app_context():
        db.create_all()
    
    from . import routes
    app.register_blueprint(routes.bp)

    return app
