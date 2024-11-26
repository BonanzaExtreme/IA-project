# app/__init__.py

from flask import Flask

def create_app():
    # Initialize the Flask app
    app = Flask(__name__, template_folder='../templates', static_folder='../static' )

    # Import and register routes
    from . import routes
    app.register_blueprint(routes.bp)

    return app
