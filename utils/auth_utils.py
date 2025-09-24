from typing import Annotated
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from prisma import Prisma
from utils.token import decode_token
from utils.encrypt import check_password
from user.models.user import LoggedUser

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

db = Prisma()

async def authenticate_user(email: str, password: str):
    await db.connect()
    user = await db.user.find_first(where={'email': email})
    await db.disconnect()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    
    if not check_password(password, user.password):
        raise HTTPException(status_code=401, detail="Error en datos de acceso.")
         
    loginUser = {
        "email": user.email,
        "id": user.id,
        "role": user.role,
        "fullname": user.fullname
    }

    return loginUser


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> LoggedUser:
    payload = decode_token(token)
    user = payload.get("sub")
    if user is None:
        raise HTTPException(status_code=401, detail="Error en datos de acceso.")
    return user


def is_admin(token: str) -> bool:
    payload = decode_token(token)
    user = LoggedUser(**payload.get("sub"))
    if user is None:
        return False
    
    if user.role != 'ADMIN':
       return False
   
    return True
    