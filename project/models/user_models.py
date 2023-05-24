# /project/models/user_models.py

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

from pydantic import validator, EmailStr
from enum import Enum

import datetime

class UserTypes( Enum):
    STUDENT = 'STUDENT'
    STAFF = 'STAFF'
    ADMIN ='ADMIN'

class UserDetails( SQLModel, table=True):
    id: Optional[int] = Field( primary_key=True)
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    user_id: Optional[int] = Field(default=None, foreign_key='user.id')
    user: Optional['User'] = Relationship(back_populates='user_details')
    
class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    # username: str = Field(index=True)
    password: str = Field(max_length=256, min_length=6)
    email: EmailStr = Field(index=True)
    first_name: str = Field(max_length=100,min_length=1)
    last_name: str = Field(max_length=100,min_length=1)
    created_at: datetime.datetime = datetime.datetime.now()
    user_type: Optional[UserTypes] 
    user_details: Optional[UserDetails] = Relationship(back_populates='user')

    processes: List["Process"] = Relationship( back_populates="student")

class UserInput(SQLModel):
    # username: str
    first_name: str
    last_name: str
    password: str = Field(max_length=256, min_length=6)
    password2: str
    email: EmailStr
    user_type: Optional[UserTypes] = UserTypes.STUDENT

    @validator('password2')
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords don\'t match')
        return v


class UserLogin(SQLModel):
    # username: str
    email: EmailStr
    password: str