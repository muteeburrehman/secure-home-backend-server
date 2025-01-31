from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
