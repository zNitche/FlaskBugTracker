from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import flask_migrate
import flask_login
import os
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


def init_database_data(models):
    from flask_bug_tracker.utils import db_utils, account_utils

    if len(models.PermissionGroup.query.all()) == 0:
        user_group = models.PermissionGroup(name=PermissionGroupsConsts.USER_GROUP)
        admin_group = models.PermissionGroup(name=PermissionGroupsConsts.ADMIN_GROUP)

        db_utils.add_object_to_db(user_group)
        db_utils.add_object_to_db(admin_group)

    if len(models.User.query.all()) == 0:
        admin_username = os.environ.get("BUILD_IN_ADMIN_USERNAME")
        admin_password = os.environ.get("BUILD_IN_ADMIN_PASSWORD")

        admin_password = account_utils.hash_password(admin_password)

        admin = models.User(username=admin_username, email=admin_username, password=admin_password,
                            permission_group_id=PermissionGroupsConsts.ADMIN_GROUP_ID)

        db_utils.add_object_to_db(admin)


def register_blueprints(app):
    from flask_bug_tracker.blueprints.auth.routes import auth
    from flask_bug_tracker.blueprints.main_app.routes import main_app
    from flask_bug_tracker.blueprints.errors.routes import errors
    from flask_bug_tracker.blueprints.admin.routes import admin

    app.register_blueprint(main_app)
    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(errors)


def create_app():
    app = Flask(__name__, instance_relative_config=False)

    app.secret_key = os.urandom(25)
    app.config.from_object("config.Config")

    db.init_app(app)

    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)

    from flask_bug_tracker import models

    @login_manager.user_loader
    def user_loader(user_id):
        return models.User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

        init_database_data(models)

        init_migrations(app)
        register_blueprints(app)

        return app
