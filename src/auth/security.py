import bcrypt


def hash_password(password: str) -> str:
    pw = bytes(password, "utf-8")
    return bcrypt.hashpw(pw, bcrypt.gensalt())


def check_password(password: str, password_in_db: str) -> bool:
    password_bytes = bytes(password, "utf-8")
    return bcrypt.checkpw(password_bytes, password_in_db)
