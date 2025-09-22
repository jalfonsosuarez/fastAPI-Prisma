import bcrypt

def get_password_hash(password: str) -> str:
    """
    Genera un hash seguro para la contraseña._

    Args:
        password (str): contraseña a encriptar

    Returns:
        str: hahs para la contraseña
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    return hashed.decode('utf-8')

def check_password(password: str, hash: str) -> bool:
    """
    Comprueba si la contraseña y el has son iguales.

    Args:
        password (str): contraseña sin encriptar
        hash (str): hash de la contraseña

    Returns:
        bool: True si contraseña y hash coinciden
    """
    ok = bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))
    
    return ok

