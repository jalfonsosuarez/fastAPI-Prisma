from pydantic import BaseModel

class Auth_Model(BaseModel):
    email: str
    password: str