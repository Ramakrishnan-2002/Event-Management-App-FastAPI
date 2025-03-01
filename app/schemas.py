from pydantic import BaseModel,EmailStr
from datetime import date,time

class UserCreateModel(BaseModel):
    username:str
    email:EmailStr
    password:str 

class Token(BaseModel):
    access_token:str
    token_type:str


class TokenResponseData(BaseModel):
    id: int
    email :EmailStr

class EventCreateModel(BaseModel):
    title:str
    description : str
    startDate :date
    startTime: time
    endDate : date
    endTime : time

class UserOut(BaseModel):
    username:str
    email:EmailStr
class ForgotEmail(BaseModel):
    email:EmailStr

class ResetPassword(BaseModel):
    token: str
    new_password: str


class DeleteEvent(BaseModel):
    title:str
    description:str