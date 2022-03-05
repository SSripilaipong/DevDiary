import bcrypt

from domain.identity.value_object.password import Password


def check_password(password: Password, password_hashed: bytes) -> bool:
    return bcrypt.checkpw(password.str().encode('ascii'), password_hashed)


def hash_password(password: Password) -> bytes:
    return bcrypt.hashpw(password.str().encode('ascii'), bcrypt.gensalt())
