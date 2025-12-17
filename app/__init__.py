import os
from flask import Flask, redirect, url_for
from config import Config
from extensions import db, migrate
from app.routes.users import users_router

def create_app(config_class: type[Config] = Config):
    # Get absolute path to the app package directory
    app_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(app_dir, 'templates')
    static_dir = os.path.join(app_dir, 'static')
    
    # Initialize Flask with absolute paths to ensure templates are found
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)


    app.register_blueprint(users_router)

    @app.route("/")
    def home():
        return redirect(url_for("users.index"))
    
    return app
