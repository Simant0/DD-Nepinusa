# /project/models/school_models.py

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


# School model
class School( SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str = Field( index=True)
    address: str
    description: str
    is_available: bool = True
    
    processes: List["Process"] = Relationship( back_populates="school")

# School model when making a patch request
class SchoolPatch(SQLModel):
    name: Optional[str]
    address: Optional[str]
    description: Optional[str]
    is_available: Optional[bool]
    
    