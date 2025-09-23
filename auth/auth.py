from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from prisma import Prisma
from .models.auth_model import Auth_Model
from utils.token import create_access_token, decode_token
from utils.encrypt import check_password
from user.models.user import LoggedUser
from uuid import UUID

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

authAPI = APIRouter(
    tags=['Auth']
)

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


def get_current_user(token: str = Depends(oauth2_scheme)) -> LoggedUser:
    payload = decode_token(token)
    user = payload.get("sub")
    if user is None:
        raise HTTPException(status_code=401, detail="Error en datos de acceso.")
    
    return user
    
def check_admin( user: LoggedUser = Depends(get_current_user)):
    if user.role != 'ADMIN':
       raise HTTPException(status_code=401, detail="No tienes permisos par acceder.")
   
    return user 

@authAPI.post("/auth")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Error en datos de acceso.")
    
    access_token = create_access_token(data={"sub": user})
    return {
        "user": user,
        "access_token": access_token,
        "token_type": "bearer"
    }
    
