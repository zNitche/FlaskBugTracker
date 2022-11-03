from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import flask_migrate
import flask_login
import os
from config import Config
from flask_bug_tracker.consts import PermissionGroupsConsts


db = SQLAlchemy()
migrate = Migrate(compare_type=True)


def init_migrations(app):
    migrations_dir_path = app.config["MIGRATIONS_DIR_PATH"]

    migrate.init_app(app, db, directory=migrations_dir_path)

    if not os.path.exists(migrations_dir_path):
        flask_migrate.init(migrations_dir_path)

    flask_migrate.migrate(migrations_dir_path)
    flask_migrate.upgrade(migrations_dir_path)


def init_database_data():
    from flask_bug_tracker.utils import db_utils, account_utils

    admin_username = os.environ.get("BUILD_IN_ADMIN_USERNAME")
    admin_password = os.environ.get("BUILD_IN_ADMIN_PASSWORD")

    account_utils.init_buildin_permissions_groups()
    account_utils.init_buildin_account(admin_username, admin_password)


def register_blueprints(app):
    from flask_bug_tracker.blueprints.auth.routes import auth
    from flask_bug_tracker.blueprints.main_app.routes import main_app
    from flask_bug_tracker.blueprints.errors.routes import errors
    from flask_bug_tracker.blueprints.admin.routes import admin
    from flask_bug_tracker.blueprints.issues.routes import issues
    from flask_bug_tracker.blueprints.projects.routes import projects
    from flask_bug_tracker.blueprints.download.routes import download

    app.register_blueprint(main_app)
    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(errors)
    app.register_blueprint(issues)
    app.register_blueprint(projects)
    app.register_blueprint(download)


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=False)

    app.secret_key = os.urandom(25)
    app.config.from_object(config_class)

    db.init_app(app)

    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)

    from flask_bug_tracker import models

    @login_manager.user_loader
    def user_loader(user_id):
        return models.User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

        init_database_data()

        if not app.config["TESTING"]:
            init_migrations(app)

        register_blueprints(app)

        return app
