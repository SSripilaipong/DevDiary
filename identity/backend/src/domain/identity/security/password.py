import bcrypt


def check_password(password: str, password_hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode('ascii'), password_hashed)


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode('ascii'), bcrypt.gensalt())
