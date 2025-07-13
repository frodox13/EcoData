import bcrypt

def hash_password(password: str) -> bytes:
    # Genera un hash seguro para la contraseña usando bcrypt.
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password: str, hashed: bytes) -> bool:
    # Verifica si la contraseña coincide con el hash almacenado.
    return bcrypt.checkpw(password.encode('utf-8'), hashed)
