import dotenv
import os
import multiprocessing


dotenv.load_dotenv(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".env"))


class Config:
    CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
    APP_DIR_PATH = os.path.join(CURRENT_DIR, "flask_bug_tracker")
    MIGRATIONS_DIR_PATH = os.path.join(CURRENT_DIR, "migrations")

    APP_PORT = 8080
    APP_HOST = "0.0.0.0"
    DEBUG_MODE = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MYSQL_DATABASE_PASSWORD = os.environ.get("MYSQL_ROOT_PASSWORD")
    MYSQL_DATABASE_ADDRESS = os.environ.get("MYSQL_SERVER_HOST")
    MYSQL_DATABASE_NAME = os.environ.get("MYSQL_DATABASE_NAME")

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:{MYSQL_DATABASE_PASSWORD}@{MYSQL_DATABASE_ADDRESS}/" \
                              f"{MYSQL_DATABASE_NAME}"

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": multiprocessing.cpu_count() - 1 + 10,
        "pool_recycle": 10,
        "pool_pre_ping": True
    }

    APP_VERSION = "v0.1"
