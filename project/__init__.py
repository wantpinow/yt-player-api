from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from credentials import app_secret_key, git_webhook_secret

# init SQLAlchemy so we can use it later in our models
# Order matters: Initialize SQLAlchemy before Marshmallow
db = SQLAlchemy()
ma = Marshmallow()


def create_app():
    app = Flask(__name__)
    # CORS(app, resources={r"/*": {"origins": "*"}})
    CORS(app, resources={r"/*": {"origins": "*"}})

    app.config['SECRET_KEY'] = app_secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['GITHUB_WEBHOOK_SECRET'] = git_webhook_secret

    db.init_app(app)
    ma.init_app(app)

    # Blueprint for each section of the API
    with app.app_context():
        # Auth
        from project.auth.auth_api import auth_blueprint as auth_blueprint
        app.register_blueprint(auth_blueprint)

        # Content
        from project.content.content_api import content_blueprint as content_blueprint
        app.register_blueprint(content_blueprint)
        
        # Git Tools
        from project.git.git_api import git_blueprint as git_blueprint
        app.register_blueprint(git_blueprint)
        

        return app
