from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(password):
    return generate_password_hash(password)


def compare_password_with_hash(password, password_hash):
    return check_password_hash(password_hash, password)


def check_if_admin(user):
    pass
