# from jose import jwt
import jwt
from jose.exceptions import JWTError
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone
from typing import Optional
from config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


if SECRET_KEY is None or ALGORITHM is None or ACCESS_TOKEN_EXPIRE_MINUTES is None:
    raise RuntimeError("SECRET_KEY, ALGORITHM  y ACCESS_TOKEN_EXPIRE_MINUTES deben estar definidos en las variables de entorno.")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """_
    Genera un token. 

    Args:
        data (dict): datos a tokenizar
        expires_delta (Optional[timedelta], optional): tiempo de exporacion del token

    Returns:
        str: token generado.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)))
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_token(token: str):
    """
    Decodifica y comprueba el token.

    Args:
        token (str): Token a validar,

    Raises:
        Exception: Si ocurre un error al validar el token.

    Returns:
        dict: datos del usuario que estaban el el token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM) # type: ignore
        return payload
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Token no válido o expirado!!!!: {e}")
    
