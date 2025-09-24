from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from utils.auth_utils import authenticate_user
from utils.token import create_access_token
from .models.auth_model import Token


authAPI = APIRouter(
    tags=['Login']
)


@authAPI.post("/auth", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Error en datos de acceso.")
    
    access_token = create_access_token(data={"sub": user})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    
