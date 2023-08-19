from pydantic import BaseModel, Field, EmailStr
from bson.objectid import ObjectId

from typing import Optional

import datetime

from enum import Enum

### Enums------------------------------------------------------------
class UserTypes( Enum):
    STUDENT = 'STUDENT'
    ADMIN ='ADMIN'
    GOD = 'GOD'
    
    def __str__(self):
        return str(self.value)

class Gender( Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    OTHERS = 'OTHERS'
    
    def __str__(self):
        return str(self.value)
###------------------------------------------------------------------

### Models-------------------------------------------------------------
class Files( BaseModel):
    url: str
    name: str
    type: str
    created_at: datetime.datetime = datetime.datetime.now()

class PersonalDetails( BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    gender: Gender
    date_of_birth: str
    profile_picture: Optional[Files | None] = None

class ContactDetails( BaseModel):
    email: list[EmailStr]
    mobile: Optional[list[str]] = None
    emergency_contact: Optional[list[str]] = None

class AddessDetails( BaseModel):
    street: Optional[str]
    city: Optional[str]
    province: Optional[str]
    zip: Optional[str]

class ApplicationDetails( BaseModel):
    graduation_date: Optional[str]
    gpa: Optional[str]
    high_school_major: Optional[str]
    intended_first_major: Optional[str]
    intended_second_major: Optional[str]

class SelectedUniversities( BaseModel):
    name: str
    url: str
    status: str
    
class SelectedServices( BaseModel):
    name: str
    description: str
    status: str


class UserDetails( BaseModel):
    personal: PersonalDetails
    contact: ContactDetails
    address: Optional[AddessDetails] = None
    application: Optional[ApplicationDetails] = None
    files: list[ Files] | None = None
    universities: list[ SelectedUniversities] | None = None
    services: list[ SelectedServices] | None = None
    created_at: datetime.datetime = datetime.datetime.now()
    last_updated: datetime.datetime = None

class User( BaseModel):
    _id: ObjectId
    username: str = Field( min_length=4, max_length=16)
    email: EmailStr
    password: str
    user_type: UserTypes
    user_details: UserDetails
    created_at: datetime.datetime = datetime.datetime.now()

    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "_id": "64d072db0515e562d32a5e1b",
                    "username": "Toby",
                    "email": "Toby@student.com",
                    "password": "password",
                    "user_type": "STUDENT",
                    "user_details": {
                        "personal": {
                        "first_name": "Tobi",
                        "last_name": "Masenju",
                        "middle_name": "Ra",
                        "gender": "MALE",
                        "date_of_birth": "02-10-2001",
                        "profile_picture": {
                            "url": "xyz/sj4kj7caw1/profile_pic.jpg",
                            "name": "profile picture",
                            "type": "jpg",
                            "created_at": "2023-08-06T19:00:13.321472"
                        }
                        },
                        "contact": {
                        "email": [
                            "tobi@student.com",
                            "tboi@gmail.com"
                        ],
                        "mobile": [
                            "9987769878"
                        ],
                        "emergency_contact": [
                            "8876679111"
                        ]
                        },
                        "address": {
                        "street": "yuor  hoem",
                        "city": "knoha",
                        "province": "FI",
                        "zip": "99809"
                        },
                        "application": {
                        "graduation_date": "10-23-2022",
                        "gpa": "4.0",
                        "high_school_major": "Science",
                        "intended_first_major": "Physics",
                        "intended_second_major": "Biology"
                        },
                        "files": [
                        {
                            "url": "xyz/asadw13fwe4df/transcript.pdf",
                            "name": "transcript",
                            "type": "pdf",
                            "created_at": "2023-08-07T21:48:14.680000"
                        },
                        {
                            "url": "xyz/asadw13fwe4df/SOP.pdf",
                            "name": "SOP",
                            "type": "pdf",
                            "created_at": "2023-08-07T21:48:14.680000"
                        }
                        ],
                        "universities": [
                        {
                            "name": "Mock State University",
                            "url": "nepseui.com/schools/2",
                            "status": "Accepted"
                        },
                        {
                            "name": "Test State University",
                            "url": "nepseui.com/schools/1",
                            "status": "Applied"
                        }
                        ],
                        "services": [
                        {
                            "name": "VISA interview",
                            "description": "book visa interview",
                            "status": "Booked"
                        }
                        ],
                        "created_at": "2023-08-07T21:48:14.688000",
                        "last_updated": "2023-08-08T02:49:18.676000"
                    },
                    "created_at": "2023-08-06T23:17:57.019000"
                }
            ]
        }
    }

class PersonalDetailsModify( BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    gender: Optional[Gender] = None
    date_of_birth: Optional[str] = None
    profile_picture: Optional[Files | None] = None

class ContactDetailsModify( BaseModel):
    email: Optional[list[str]] = None
    mobile: Optional[list[str]] = None
    emergency_contact: Optional[list[str]] = None

class ApplicationDetailsModify( BaseModel):
    graduation_date: Optional[str] = None
    gpa: Optional[str] = None
    high_school_major: Optional[str] = None
    intended_first_major: Optional[str] = None
    intended_second_major: Optional[str] = None

class UserDetailsModify( BaseModel):
    personal: Optional[PersonalDetailsModify] = None
    contact: Optional[ContactDetailsModify] = None
    address: Optional[AddessDetails] = None
    application: Optional[ApplicationDetailsModify] = None
    # files: list[ Files] | None = None
    # universities: list[ SelectedUniversities] | None = None
    # services: list[ SelectedServices] | None = None
    last_updated: datetime.datetime = datetime.datetime.now()

class UserModify( BaseModel):
    # username: Optional[str] = None
    # email: Optional[str] = None
    # password: Optional[str] = None
    # user_type: Optional [UserTypes] = None
    user_details: Optional[UserDetailsModify] = None
### -------------------------------------------------------------------