# /project/models/process_models.py

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from enum import Enum as Enum_

import datetime

from models.school_models import School
from models.user_models import User

class Enum( Enum_):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
    
class ProcessTypes( str, Enum):
    APPLY = 'APPLY'
    TEST_BOOKING = 'TEST BOOKING'
    WRITING = 'WRITING'
    VISA = 'VISA' 

class ProcessStatus( str, Enum):
    DRAFT = 'DRAFT'
    SUBMIT = 'SUBMIT'
    IN_PROGRESS = 'IN PROGRESS'
    WAITING = 'WAITING'
    COMPLETED = 'COMPLETED'

class Process( SQLModel, table=True):
    id : Optional[int] = Field( primary_key=True)
    title: str = Field( index=True)
    process_type: Optional[ProcessTypes] = None
    status: Optional[ProcessStatus] = ProcessStatus.DRAFT
    school_id: Optional[int] = Field(default=None, foreign_key='school.id') 
    school: Optional[School] = Relationship(back_populates='processes')
    notes: Optional[str] = None
    created_at: datetime.datetime = datetime.datetime.now()
    last_modified: datetime.datetime = datetime.datetime.now()
    student_id: Optional[int] = Field(default=None, foreign_key='user.id')
    student: Optional[User] = Relationship()
    
class ProcessPatch( SQLModel):
    id : Optional[int] = Field( primary_key=True)
    process_type: Optional[ProcessTypes] = None
    school_id: Optional[int] = Field(default=None, foreign_key='school.id') 
    status: Optional[ProcessStatus] = None
    notes: Optional[str] = None
    last_modified: Optional[datetime.datetime]
    student_id: Optional[int] = Field(default=None, foreign_key='user.id')
    student: Optional[User] = Relationship()

