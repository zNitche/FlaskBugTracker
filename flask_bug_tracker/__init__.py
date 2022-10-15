from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import flask_migrate
import os


db = SQLAlchemy()
migrate = Migrate(compare_type=True)


def register_blueprints(app):
    from flask_bug_tracker.routes import content, errors

    app.register_blueprint(content.content)
    app.register_blueprint(errors.errors)


def init_migrations(app):
    migrations_dir_path = app.config["MIGRATIONS_DIR_PATH"]

    migrate.init_app(app, db, directory=migrations_dir_path)

    if not os.path.exists(migrations_dir_path):
        flask_migrate.init(migrations_dir_path)

    flask_migrate.migrate(migrations_dir_path)
    flask_migrate.upgrade(migrations_dir_path)


def create_app():
    app = Flask(__name__, instance_relative_config=False)

    app.secret_key = os.urandom(25)
    app.config.from_object("config.Config")

    db.init_app(app)

    from flask_bug_tracker import models

    with app.app_context():
        db.create_all()

        init_migrations(app)
        register_blueprints(app)

        return app
