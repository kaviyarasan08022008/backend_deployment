from pydantic import BaseModel

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    user_name: str
    state: str
    password: str
    district: str
    village_town: str | None = None
    user_role: str
    phone_number:  str   # admin / collector / user

class UserCreate(BaseModel):
    state: str
    district: str
    village_town: str

class UserLogin(BaseModel):
    user_name: str
    password: str
    user_role: str
   

