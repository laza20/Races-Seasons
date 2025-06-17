from pydantic import BaseModel, Field, EmailStr, conint
from typing import Annotated


class UserCreate(BaseModel):
    id        : str | None = None
    name      : str
    surname   : str
    username : str
    age       : int
    mail      : EmailStr
    password  : str = Field(..., min_length=8)
    estado    : bool | None = None

class User(BaseModel):
    id        : str | None = None
    name      : str
    surname   : str
    username : str
    age       : Annotated[int, conint(ge=12)] #edad mayor a 12
    mail      : EmailStr
    estado    : bool
    
class UserLogin(BaseModel):
    mail      : str
    password  : str
    estado    : bool

class UserPassword(BaseModel):
    password  : str = Field(..., min_length=8, description="La contraseña debe tener al menos 8 caracteres.")
    